# 文件说明：tokio-test 宏集合

## 文件目的
该文件提供了用于测试 Tokio 异步代码和 Futures 的实用宏集合。通过封装常见的断言逻辑，简化异步测试的编写，确保测试代码简洁且易于维护。

---

## 核心组件

### 1. `assert_ready!` 宏
- **功能**：断言 `Poll` 结果为 `Ready`，返回值。
- **实现**：
  ```rust
  macro_rules! assert_ready {
      ($e:expr) => {{
          match $e {
              Poll::Ready(v) => v,
              Poll::Pending => panic!("pending"),
          }
      }};
      // 支持自定义报错信息
      ($e:expr, $($msg:tt)+) => {{
          match $e {
              Poll::Ready(v) => v,
              Poll::Pending => panic!("pending; {}", format_args!($($msg)+)),
          }
      }};
  }
  ```
- **使用场景**：验证 Future 是否立即完成（如 `future::ready`）。

---

### 2. `assert_ready_ok!` 和 `assert_ready_err!`
- **功能**：断言 `Poll<Result<...>>` 的结果为 `Ready(Ok(...))` 或 `Ready(Err(...))`。
- **实现**：
  ```rust
  // assert_ready_ok! 内部调用 assert_ready! 和 assert_ok!
  macro_rules! assert_ready_ok {
      ($e:expr) => {{
          let val = assert_ready!($e);
          assert_ok!(val)
      }};
  }
  ```
- **使用场景**：测试返回 `Result` 类型的 Future（如网络请求）。

---

### 3. `assert_pending!`
- **功能**：断言 `Poll` 结果为 `Pending`。
- **实现**：
  ```rust
  macro_rules! assert_pending {
      ($e:expr) => {{
          match $e {
              Poll::Pending => {}
              Poll::Ready(v) => panic!("ready; value = {:?}", v),
          }
      }};
  }
  ```
- **使用场景**：验证 Future 是否未完成（如 `future::pending`）。

---

### 4. `assert_ready_eq!`
- **功能**：同时断言 `Poll` 为 `Ready` 并验证返回值与预期值相等。
- **实现**：
  ```rust
  macro_rules! assert_ready_eq {
      ($e:expr, $expect:expr) => {{
          let val = assert_ready!($e);
          assert_eq!(val, $expect)
      }};
  }
  ```
- **使用场景**：测试 Future 返回的具体值（如 `future::ready(42)`）。

---

### 5. `assert_ok!` 和 `assert_err!`
- **功能**：断言 `Result` 类型为 `Ok` 或 `Err`。
- **实现**：
  ```rust
  // assert_ok! 示例
  macro_rules! assert_ok {
      ($e:expr) => {{
          match $e {
              Ok(v) => v,
              Err(e) => panic!("assertion failed: Err({:?})", e),
          }
      }};
  }
  ```
- **使用场景**：非 Future 场景下的结果验证（如解析字符串为数字）。

---

### 6. `assert_elapsed!`
- **功能**：断言时间差在预期值 ±1ms 范围内。
- **实现**：
  ```rust
  macro_rules! assert_elapsed {
      ($start:expr, $dur:expr) => {{
          let elapsed = $start.elapsed();
          assert!(
              elapsed >= $dur && elapsed <= $dur + Duration::from_millis(1),
              "actual = {:?}, expected = {:?}",
              elapsed,
              $dur
          );
      }};
  }
  ```
- **使用场景**：测试异步定时任务（如 `tokio::time::sleep`）。

---

## 项目中的角色