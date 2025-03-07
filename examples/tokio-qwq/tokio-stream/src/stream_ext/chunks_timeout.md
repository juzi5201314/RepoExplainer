rust
use crate::stream_ext::Fuse;
use crate::Stream;
use tokio::time::{sleep, Sleep};
use core::future::Future;
use core::pin::Pin;
use core::task::{ready, Context, Poll};
use pin_project_lite::pin_project;
use std::time::Duration;

pin_project! {
    /// Stream returned by the [`chunks_timeout`](super::StreamExt::chunks_timeout) method.
    #[must_use = "streams do nothing unless polled"]
    #[derive(Debug)]
    pub struct ChunksTimeout<S: Stream> {
        #[pin]
        stream: Fuse<S>,
        #[pin]
        deadline: Option<Sleep>,
        duration: Duration,
        items: Vec<S::Item>,
        cap: usize,
    }
}

impl<S: Stream> ChunksTimeout<S> {
    pub(super) fn new(stream: S, max_size: usize, duration: Duration) -> Self {
        ChunksTimeout {
            stream: Fuse::new(stream),
            deadline: None,
            duration,
            items: Vec::with_capacity(max_size),
            cap: max_size,
        }
    }
}

impl<S: Stream> Stream for ChunksTimeout<S> {
    type Item = Vec<S::Item>;

    fn poll_next(mut self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Option<Self::Item>> {
        let mut me = self.as_mut().project();
        loop {
            match me.stream.as_mut().poll_next(cx) {
                Poll::Pending => break,
                Poll::Ready(Some(item)) => {
                    if me.items.is_empty() {
                        me.deadline.set(Some(sleep(*me.duration)));
                        me.items.reserve_exact(*me.cap);
                    }
                    me.items.push(item);
                    if me.items.len() >= *me.cap {
                        return Poll::Ready(Some(std::mem::take(me.items)));
                    }
                }
                Poll::Ready(None) => {
                    let last = if me.items.is_empty() {
                        None
                    } else {
                        Some(std::mem::take(me.items))
                    };
                    return Poll::Ready(last);
                }
            }
        }

        if !me.items.is_empty() {
            if let Some(deadline) = me.deadline.as_pin_mut() {
                ready!(deadline.poll(cx));
            }
            return Poll::Ready(Some(std::mem::take(me.items)));
        }

        Poll::Pending
    }

    fn size_hint(&self) -> (usize, Option<usize>) {
        let chunk_len = if self.items.is_empty() { 0 } else { 1 };
        let (lower, upper) = self.stream.size_hint();
        let lower = (lower / self.cap).saturating_add(chunk_len);
        let upper = upper.and_then(|x| x.checked_add(chunk_len));
        (lower, upper)
    }
}
```

---

### 代码文件解释

#### **文件目的**
该文件实现了 `ChunksTimeout` 流适配器，用于将输入流的元素分块收集，并在达到指定最大块大小或超时时间时返回当前块。它结合了 **批量处理** 和 **超时机制**，适用于需要定期或按需处理数据块的场景（如网络数据包分批传输、日志聚合等）。

---

#### **关键组件**

1. **结构体 `ChunksTimeout<S>`**
   - **字段说明**：
     - `stream`: 被包装的原始流，使用 `Fuse` 自动处理流的结束状态。
     - `deadline`: 超时计时器（`Sleep` 类型的异步任务）。
     - `duration`: 超时时间间隔。
     - `items`: 当前正在收集的元素列表。
     - `cap`: 每个块的最大元素数量。
   - **功能**：通过 `pin_project` 宏管理内部字段的指针，支持异步操作的 `Pin` 和 `Projection`。

2. **构造函数 `new`**
   - 初始化 `ChunksTimeout` 实例，设置初始参数：
     - 将输入流包装为 `Fuse` 以避免重复轮询结束的流。
     - 预分配 `items` 的容量以优化性能。

3. **`poll_next` 方法**
   - **核心逻辑**：
     1. 持续轮询底层流，直到遇到 `Pending`（无新元素）或流结束。
     2. **收集元素**：每当接收到新元素时，将其添加到 `items` 中。
     3. **触发条件**：
        - **块满**：当 `items` 达到 `cap` 时，立即返回当前块。
        - **流结束**：若流结束且 `items` 非空，则返回剩余元素。
        - **超时**：若 `items` 非空且超时时间到达，则返回当前块。
     4. **超时处理**：首次添加元素时启动超时计时器，若超时则强制返回当前块。
   - **返回值**：返回当前收集的块（`Vec<S::Item>`）或 `None`（流结束且无剩余元素）。

4. **`size_hint` 方法**
   - 根据当前已收集的元素和底层流的 `size_hint`，估算剩余块的数量范围。

---

#### **实现细节**
- **超时机制**：通过 `sleep(duration)` 创建异步计时器，当首次添加元素时启动计时器，并在每次 `poll` 时检查是否超时。
- **自动熔断**：使用 `Fuse` 包装流，避免在流结束后重复轮询。
- **性能优化**：预分配 `items` 的容量（`reserve_exact`），减少内存分配开销。

---

#### **项目中的角色**