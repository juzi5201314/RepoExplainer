# `fuzz_stream_map.rs` 文件详解

## 文件目的
该文件是一个模糊测试（Fuzz Testing）目标，用于测试 Tokio 的 `StreamMap` 类型在不同输入条件下的正确性和稳定性。通过随机生成的布尔数组配置，验证 `StreamMap` 在添加不同状态流（空流或挂起流）时的行为是否符合预期。

---

## 核心组件与逻辑

### 1. **依赖与宏定义**
- **依赖库**：
  - `libfuzzer_sys`：提供模糊测试框架支持。
  - `tokio_stream`：Tokio 流框架的核心模块。
  - `tokio_test`：用于流的测试工具（如 `task::spawn`、`assert_pending` 等）。
- **自定义宏**：
  - `assert_ready_none!`：断言流的 `poll_next` 返回 `Poll::Ready(None)`，否则抛出错误。

### 2. **辅助函数**
- **`pin_box` 函数**：
  ```rust
  fn pin_box<T: Stream<Item = U> + 'static, U>(s: T) -> Pin<Box<dyn Stream<Item = U>>> {
      Box::pin(s)
  }
  ```
  将具体流类型包装为 `Pin<Box<dyn Stream>>`，以便作为 trait 对象插入 `StreamMap`。

### 3. **`DidPoll` 结构体**
```rust
struct DidPoll<T> {
    did_poll: bool,
    inner: T,
}
```
- **作用**：包装流并记录是否被轮询（`poll_next` 被调用）。
- **实现 `Stream` trait**：
  ```rust
  fn poll_next(...) {
      self.did_poll = true;
      Pin::new(&mut self.inner).poll_next(cx)
  }
  ```
  在调用内部流的 `poll_next` 前标记 `did_poll` 为 `true`。

---

### 4. **模糊测试逻辑**
```rust
fuzz_target!(|data: [bool; 64]| {
    for len in 0..data.len() {
        // 初始化 StreamMap
        let mut map = task::spawn(StreamMap::new());
        let mut expect = 0;

        // 根据输入数据配置流
        for (i, is_empty) in data[..len].iter().copied().enumerate() {
            let inner = if is_empty {
                pin_box(stream::empty::<()>())
            } else {
                expect += 1;
                pin_box(stream::pending::<()>())
            };
            map.insert(i, DidPoll { did_poll: false, inner });
        }

        // 验证 StreamMap 行为
        if expect == 0 {
            assert_ready_none!(map.poll_next());
        } else {
            assert_pending!(map.poll_next()); // 应挂起
            assert_eq!(expect, map.values().count()); // 校验流数量
            for stream in map.values() {
                assert!(stream.did_poll); // 确保所有流被轮询
            }
        }
    }
});
```

#### 关键步骤说明：
1. **输入配置**：
   - 输入是长度为 64 的布尔数组 `data`，每个元素决定对应流是否为空（`true`）或挂起（`false`）。
   - 通过遍历 `len`（从 `0` 到 `63`），测试不同长度的输入。

2. **流构建**：
   - 若 `is_empty` 为 `true`，插入空流（`stream::empty`）。
   - 否则插入挂起流（`stream::pending`），并增加 `expect` 计数（表示预期有值的流数量）。

3. **行为验证**：
   - **无有效流**：若 `expect == 0`，`poll_next` 应立即返回 `None`。
   - **存在有效流**：
     - `poll_next` 应返回 `Poll::Pending`（因挂起流未完成）。
     - 所有插入的流必须被轮询（通过 `did_poll` 标记验证）。

---

## 在项目中的角色