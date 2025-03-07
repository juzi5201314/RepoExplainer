# `custom-executor-tokio-context.rs` 文件详解

## **文件目的**
该示例演示了如何通过 Tokio 的 `RuntimeExt` 扩展，在不支持特定功能的运行时中，通过嵌套其他运行时的执行器来补充缺失的功能。具体展示了如何在缺少定时器（timer）的运行时中，通过包装另一个启用定时器的运行时来避免 panic。

---

## **关键组件与实现**

### **1. 运行时配置**
- **`rt1`（主运行时）**：
  ```rust
  let rt1 = Builder::new_multi_thread()
      .worker_threads(1)
      .build()
      .unwrap();
  ```
  - 配置为单线程多线程运行时，但**未启用定时器**（`no timer`）。
  - 用于演示在基础功能受限的运行时中执行任务。

- **`rt2`（辅助运行时）**：
  ```rust
  let rt2 = Builder::new_multi_thread()
      .worker_threads(1)
      .enable_all()
      .build()
      .unwrap();
  ```
  - 启用所有功能（包括定时器），提供必要的补充能力。

---

### **2. 执行器嵌套与上下文包装**
通过 `rt2.wrap()` 将 `rt2` 的执行器上下文包装到 `rt1` 的任务中：
```rust
rt1.block_on(rt2.wrap(async move { ... }));
```
- **作用**：
  - 允许在 `rt1` 的上下文中执行 `rt2` 的任务。
  - 确保 `TcpListener::bind()` 等需要定时器的操作能正常运行（因 `rt1` 本身无定时器）。
- **关键点**：
  - 若未使用 `wrap()`，`rt1` 缺少定时器会导致 `TcpListener` 绑定时 panic。

---

### **3. 异步任务与同步**
- **TCP 监听器绑定**：
  ```rust
  let listener = TcpListener::bind("0.0.0.0:0").await.unwrap();
  println!("addr: {:?}", listener.local_addr());
  ```
  - 在 `rt2` 的上下文中绑定 TCP 端口，依赖 `rt2` 的定时器功能。
  
- **`oneshot` 通道同步**：
  ```rust
  tx.send(()).unwrap();
  futures::executor::block_on(rx).unwrap();
  ```
  - 使用 `oneshot` 通道同步主线程，确保 TCP 绑定完成后继续执行。

---

## **代码流程**
1. 创建两个运行时 `rt1`（无定时器）和 `rt2`（全功能）。
2. 在 `rt1` 的上下文中，通过 `rt2.wrap()` 包装异步任务。
3. 在包装的任务中绑定 TCP 端口（依赖 `rt2` 的定时器）。
4. 通过 `oneshot` 通道同步主线程，确保任务完成。

---

## **项目中的角色**