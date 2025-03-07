# 文件说明：`tokio/src/signal/ctrl_c.rs`

## **目的**  
提供跨平台的异步 API，用于监听进程接收到的 **Ctrl-C** 信号（SIGINT）。该文件封装了 Unix 和 Windows 系统下不同的信号处理机制，允许开发者通过统一的接口实现信号监听。

---

## **关键组件**

### **1. 平台适配**
- 使用 `cfg` 宏根据操作系统引入不同实现：
  - **Unix**：通过 `super::unix` 模块实现。
  - **Windows**：通过 `super::windows` 模块实现。
- 通过 `os_impl` 命名空间隐藏平台差异，确保代码逻辑统一。

### **2. 核心函数 `ctrl_c()`**
```rust
pub async fn ctrl_c() -> io::Result<()> {
    os_impl::ctrl_c()?.recv().await;
    Ok(())
}
```
- **功能**：返回一个异步 Future，当进程接收到 **Ctrl-C** 信号时完成。
- **实现细节**：
  - 调用 `os_impl::ctrl_c()` 获取平台相关的信号流（Stream）。
  - 通过 `recv().await` 等待信号事件。
  - 成功时返回 `Ok(())`，错误时返回 `io::Error`。

### **3. 平台行为说明**
- **Unix**：
  - 首次注册信号监听时，会替换系统默认的信号处理行为（如终止进程）。
  - 即使信号监听器被丢弃，Tokio 仍会捕获后续信号，**不会恢复默认行为**。
- **Windows**：
  - 通过 `CtrlC` 等结构体处理信号，与 Unix 实现逻辑隔离。

---

## **使用示例**
```rust,no_run
use tokio::signal;

#[tokio::main]
async fn main() {
    println!("等待 Ctrl-C...");
    signal::ctrl_c().await.expect("监听失败");
    println!("收到 Ctrl-C 信号");
}
```

---

## **注意事项**
- **Unix 平台风险**：
  - 信号处理器的安装是全局性的，可能影响其他信号监听逻辑。
  - 需确保应用正确处理信号行为（例如手动恢复默认行为）。
- **异步监听**：
  - Future 在首次 `poll` 后注册监听器，信号需在注册后触发才能生效。

---

## **项目中的角色**