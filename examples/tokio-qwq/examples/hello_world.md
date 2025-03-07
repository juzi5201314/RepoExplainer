# `hello_world.rs` 文件详解

## **文件目的**
这是一个使用 Tokio 库实现的简单 TCP 客户端示例程序。其核心功能是：
1. 连接到本地 `127.0.0.1:6142` 端口
2. 发送字符串 `hello world\n`
3. 关闭连接

用户可通过 `ncat -l 6142` 启动一个简单的 TCP 服务器来测试该客户端。

---

## **关键代码结构**

### **依赖与宏定义**
```rust
#![warn(rust_2018_idioms)] // 启用 Rust 2018 版本的代码规范检查
use tokio::io::AsyncWriteExt; // 提供异步写入方法
use tokio::net::TcpStream; // Tokio 的异步 TCP 流
use std::error::Error; // 标准错误处理 trait
```

### **异步主函数**
```rust
#[tokio::main] // 标记为 Tokio 异步主函数
pub async fn main() -> Result<(), Box<dyn Error>> {
    // 主体逻辑
}
```
- 使用 `Box<dyn Error>` 统一错误处理
- `async/await` 语法实现非阻塞异步操作

---

### **核心逻辑步骤**
#### **1. 建立 TCP 连接**
```rust
let mut stream = TcpStream::connect("127.0.0.1:6142").await?;
```
- 调用 Tokio 的 `TcpStream::connect` 建立异步连接
- `.await?` 表示等待异步操作完成并处理可能的错误

#### **2. 发送数据**
```rust
let result = stream.write_all(b"hello world\n").await;
```
- 使用 `AsyncWriteExt` 的 `write_all` 方法确保完整写入字节
- 返回 `Result` 表示操作是否成功

#### **3. 日志输出**
```rust
println!("created stream");
println!("wrote to stream; success={:?}", result.is_ok());
```
- 通过 `println!` 记录关键操作状态

---

## **项目中的角色**
该文件是 Tokio 库的入门示例，用于演示以下核心概念：
1. **异步 TCP 客户端**的实现方法
2. **Tokio 运行时**的使用（通过 `#[tokio::main]` 宏）
3. **异步 IO 操作**（连接、写入）
4. **错误处理**的 Rust 风格实践
