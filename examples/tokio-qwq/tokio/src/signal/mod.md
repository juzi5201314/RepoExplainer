# `tokio/src/signal/mod.rs` 文件详解

## 概述
该文件是 Tokio 异步信号处理模块的核心入口文件，提供跨平台的异步信号监听功能。它通过抽象 Unix 和 Windows 的信号处理差异，为开发者提供统一的 API 接口，支持在异步运行时中安全地处理操作系统信号。

## 核心功能
1. **信号监听抽象**
   - 提供 `ctrl_c()` 等跨平台信号监听接口
   - 通过 `unix` 和 `windows` 子模块实现平台特有逻辑
   - 使用观察者模式(`watch::Receiver`)实现信号通知

2. **异步信号流处理**
   - `RxFuture` 结构体通过复用 Future 对象优化性能
   - `poll_recv` 方法实现高效的信号轮询机制
   - `ReusableBoxFuture` 类型管理可复用的异步任务

3. **平台适配**
   - 通过 `os` 模块动态选择 Unix/Windows 实现
   - 提供 `SignalKind` 枚举支持 Unix 的多种信号类型（如 SIGHUP）

## 关键组件解析

### 1. 平台抽象层 (`os` 模块)
```rust
mod os {
    #[cfg(unix)]
    pub(crate) use super::unix::{OsExtraData, OsStorage};

    #[cfg(windows)]
    pub(crate) use super::windows::{OsExtraData, OsStorage};
}
```
- 根据目标平台选择对应的信号处理实现
- 统一暴露 `OsExtraData` 和 `OsStorage` 接口
- 实现信号注册、文件描述符管理等底层操作

### 2. 核心 Future 结构 (`RxFuture`)
```rust
struct RxFuture {
    inner: ReusableBoxFuture<Receiver<()>>,
}

impl RxFuture {
    fn new(rx: Receiver<()>) -> Self { /* 初始化 */ }
    async fn recv(&mut self) -> Option<()> { /* 异步接收信号 */ }
    fn poll_recv(&mut self, cx: &mut Context<'_>) -> Poll<Option<()>> { /* 轮询实现 */ }
}
```
- 使用可复用的 Future 对象减少内存分配
- 通过 `watch::Receiver` 监听信号通道
- `poll_recv` 方法实现零拷贝的信号轮询

### 3. 控制台信号接口 (`ctrl_c`)
```rust
#[cfg(feature = "signal")]
mod ctrl_c;
pub use ctrl_c::ctrl_c;
```
- 提供跨平台的控制台中断监听
- 在 Unix 通过 `SIGINT` 实现
- 在 Windows 使用控制台输入事件处理

## 使用示例
```rust
// 监听 Ctrl-C 信号
#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    signal::ctrl_c().await?;
    println!("收到终止信号!");
    Ok(())
}

// 监听 Unix 的 SIGHUP 信号
#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let mut stream = signal(SignalKind::hangup())?;
    loop {
        stream.recv().await;
        println!("收到 SIGHUP 信号");
    }
}
```

## 在项目中的角色
该文件是 Tokio 信号处理模块的核心协调者，提供跨平台的异步信号监听能力，通过抽象操作系统差异和优化异步轮询机制，使开发者能够安全高效地在异步程序中处理操作系统信号事件。
