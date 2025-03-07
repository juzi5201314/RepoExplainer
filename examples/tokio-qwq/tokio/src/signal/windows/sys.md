rust
# 该文件是 Tokio 异步运行时中用于 Windows 平台控制信号处理的核心实现。它提供了对 Windows 控制台事件（如 Ctrl+C、关闭窗口等）的异步监听支持。

## 主要功能
1. **事件监听接口**  
   提供 `ctrl_break`、`ctrl_close` 等函数，允许用户通过异步 Future 监听特定控制事件。
   ```rust
   pub(super) fn ctrl_c() -> io::Result<RxFuture> {
       new(console::CTRL_C_EVENT)
   }
   ```

2. **全局初始化**  
   通过 `global_init` 设置控制台事件处理函数，确保仅初始化一次：
   ```rust
   fn global_init() -> io::Result<()> {
       static INIT: Once = Once::new();
       // 使用 unsafe 调用 Windows API SetConsoleCtrlHandler
   }
   ```

3. **事件处理逻辑**  
   `handler` 函数是 Windows 调用的回调，负责记录事件并通知监听者：
   ```rust
   unsafe extern "system" fn handler(ty: u32) -> BOOL {
       // 记录事件并广播
       if event_was_handled && 需要无限循环 {
           loop { std::thread::park(); }
       }
       // 返回处理结果
   }
   ```

4. **事件存储管理**  
   `OsStorage` 结构体存储各事件的元数据，实现 `Storage` trait 供全局注册系统使用：
   ```rust
   impl Storage for OsStorage {
       fn event_info(&self, id: EventId) -> Option<&EventInfo> {
           // 根据事件类型返回对应 EventInfo
       }
   }
   ```

## 关键组件
- **事件类型**  
  使用 Windows API 定义的控制事件常量：
  ```rust
  use windows_sys::Win32::System::Console as console;
  // 如 console::CTRL_C_EVENT
  ```

- **异步 Future 实现**  
  通过 `new` 函数创建 `RxFuture`，注册监听并返回可等待的 Future：
  ```rust
  fn new(signum: u32) -> io::Result<RxFuture> {
      Ok(RxFuture::new(globals().register_listener(signum as EventId)))
  }
  ```

- **无限循环处理**  
  针对关闭/注销/关机事件，若被监听则进入无限循环避免进程立即终止：
  ```rust
  if event_requires_infinite_sleep_in_handler(ty) {
      loop { std::thread::park(); }
  }
  ```

## 项目中的角色