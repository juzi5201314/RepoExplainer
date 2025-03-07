### 文件说明：`peekable.rs`

#### 目的
该文件实现了 Tokio 流扩展中的 `Peekable` 适配器，允许用户在不消耗流元素的情况下预览流的下一个元素。通过 `peek()` 方法，用户可以异步获取流的下一个元素的引用，同时保持流的当前位置不变。

---

#### 核心组件

1. **结构定义 `Peekable<T>`**
   ```rust
   pin_project! {
       pub struct Peekable<T: Stream> {
           peek: Option<T::Item>,
           #[pin]
           stream: Fuse<T>,
       }
   }
   ```
   - **`peek`**：存储通过 `peek()` 方法预览的元素，类型为 `Option<T::Item>`。
   - **`stream`**：被 `Fuse` 包装的底层流，确保流在结束时不再被轮询。使用 `#[pin]` 标记以支持 `Pin` 语义。

2. **构造方法 `new`**
   ```rust
   pub(crate) fn new(stream: T) -> Self {
       let stream = stream.fuse();
       Self { peek: None, stream }
   }
   ```
   - 初始化时将流包装为 `Fuse<T>`，并清空 `peek` 缓存。

3. **预览方法 `peek()`**
   ```rust
   pub async fn peek(&mut self) -> Option<&T::Item>
   where
       T: Unpin,
   {
       if let Some(ref it) = self.peek {
           Some(it)
       } else {
           self.peek = self.next().await;
           self.peek.as_ref()
       }
   }
   ```
   - **逻辑**：若 `peek` 缓存已存在元素，直接返回引用；否则通过 `self.next().await` 获取下一个元素并缓存。
   - **依赖 `Unpin`**：由于 `Peekable` 内部包含 `Pin` 字段，要求 `T` 实现 `Unpin` 以确保引用有效性。

4. **流实现 `Stream for Peekable<T>`**
   ```rust
   fn poll_next(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Option<Self::Item>> {
       let this = self.project();
       if let Some(it) = this.peek.take() {
           Poll::Ready(Some(it))
       } else {
           this.stream.poll_next(cx)
       }
   }
   ```
   - **轮询逻辑**：优先返回 `peek` 缓存的元素（若存在），否则轮询底层流。
   - **`take()` 操作**：取出 `peek` 缓存的元素后清空缓存，确保后续调用 `next()` 正确消费流。

---

#### 项目中的作用
该文件为 Tokio 流提供了 `Peekable` 适配器，使用户能够安全地预览流的下一个元素而不改变流的状态。这一功能在需要条件处理（如根据元素内容决定后续操作）或流的惰性计算场景中非常有用，是 Tokio 异步流扩展的重要组成部分。
