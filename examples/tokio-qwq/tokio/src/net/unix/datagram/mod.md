# Unix域数据报模块说明

## 模块概述
该模块是Tokio异步运行时中Unix域套接字数据报通信的核心实现部分，负责提供基于Unix域协议的无连接数据报通信功能。通过封装底层socket接口，为异步编程环境提供高效的进程间通信支持。

## 关键组件

### 1. 核心结构体
- **UnixSocket**  
  封装了底层socket2::Socket的抽象类型，包含以下特性：
  ```rust
  #[derive(Debug)]
  pub struct UnixSocket {
      inner: socket2::Socket,
  }
  ```
  - 使用socket2库管理底层文件描述符
  - 支持异步I/O操作
  - 提供类型检查（如验证套接字类型是否为DGRAM）

### 2. 核心功能函数
- **new_datagram()**  
  创建新的Unix域数据报套接字：
  ```rust
  pub fn new_datagram() -> io::Result<UnixSocket> {
      UnixSocket::new(socket2::Type::DGRAM)
  }
  ```
  - 调用系统socket(2)系统调用，参数为AF_UNIX和SOCK_DGRAM
  - 返回异步安全的UnixSocket实例

- **from_std()**  
  将标准库的同步UnixDatagram转换为Tokio异步版本：
  ```rust
  pub fn from_std(datagram: net::UnixDatagram) -> io::Result<UnixDatagram> {
      let socket = mio::net::UnixDatagram::from_std(datagram);
      let io = PollEvented::new(socket)?;
      // ...
  }
  ```
  - 利用mio库实现异步事件监听
  - 将同步套接字包装为异步安全的PollEvented结构

### 3. 辅助模块
- **socketaddr模块**  
  提供`SocketAddr`类型用于表示Unix域地址，支持路径和抽象命名空间地址的表示。

- **ucred模块**  
  定义`UCred`结构体，用于携带进程凭证信息（用户ID、组ID、进程ID），支持安全的进程间通信。

- **stream模块**  
  处理流式套接字相关逻辑，提供与数据报套接字的类型检查（如`if self.ty() == Type::STREAM`）。

- **pipe模块**  
  提供Unix域管道的封装实现，支持进程间管道通信。

### 4. 异步操作支持
- **连接操作**  
  ```rust
  pub async fn connect(self, path: impl AsRef<Path>) -> io::Result<UnixStream> { /* ... */ }
  ```
  - 异步完成套接字连接
  - 返回UnixStream实例用于流式通信

- **读写分离**  
  ```rust
  pub mod split {
      pub use super::ReadHalf;
      pub use super::WriteHalf;
  }
  ```
  - 通过`split()`方法将套接字拆分为独立的读写半连接，支持并发操作

## 模块结构
```
├── socket.rs          // 套接字核心实现
├── socketaddr.rs      // 地址类型定义
├── ucred.rs           // 进程凭证结构
├── stream.rs          // 流式套接字逻辑
├── pipe.rs            // 管道实现
└── mod.rs             // 模块导出与核心函数
```

## 在项目中的角色