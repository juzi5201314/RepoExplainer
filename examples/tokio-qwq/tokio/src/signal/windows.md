### 文件说明：Windows平台信号处理模块

#### 目的
该模块为Tokio异步运行时提供Windows平台特定的控制台信号处理功能，支持监听Ctrl-C、Ctrl-Break、Ctrl-Logoff、Ctrl-Shutdown和Ctrl-Close等系统事件。通过Windows API `SetConsoleCtrlHandler`实现事件监听，并为每个信号类型提供异步接收接口。

#### 关键组件
1. **配置与依赖**
   - 使用`cfg`宏确保代码仅在Windows平台或文档生成时生效
   - 引入`RxFuture`类型（来自Tokio信号模块）作为底层信号接收器
   - 根据平台条件动态加载实现模块：
     ```rust
     #[cfg(windows)]
     #[path = "windows/sys.rs"]
     mod imp;
     ```

2. **信号监听器结构体**
   - 每个信号类型对应一个结构体（如`CtrlC`, `CtrlBreak`等）：
     ```rust
     pub struct CtrlC { inner: RxFuture }
     ```
   - 统一提供以下方法：
     - `recv()`：异步等待下一个信号事件
     - `poll_recv()`：手动轮询信号事件（非async场景）

3. **工厂函数**
   - 为每种信号提供创建监听器的函数（如`ctrl_c()`）：
     ```rust
     pub fn ctrl_c() -> io::Result<CtrlC> {
         Ok(CtrlC { inner: imp::ctrl_c()? })
     }
     ```

4. **信号处理特性**
   - **事件广播**：所有监听器会同时接收到同一信号事件
   - **事件合并**：短时间内连续触发的事件可能被合并为单次通知

#### 工作原理
1. 通过`SetConsoleCtrlHandler`注册事件处理回调
2. 每个监听器实例包装`RxFuture`作为信号接收通道
3. 调用`recv()`或`poll_recv()`会通过Future机制等待事件触发
4. 内部实现（`imp`模块）负责与Windows API交互和事件分发

#### 项目中的角色