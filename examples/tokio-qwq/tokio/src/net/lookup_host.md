# 文件说明：Tokio DNS解析核心实现

## 文件路径
explanations/tokio/tokio/src/net/lookup_host.rs

## 主要功能
该文件实现了Tokio异步运行时的DNS解析功能，提供了一个异步友好的接口`lookup_host`，用于将主机名和端口转换为Socket地址列表。

## 关键组件

### 1. 条件编译配置
```rust
cfg_net! { ... }
```
- 使用`cfg_net!`宏确保代码仅在支持网络功能的平台上编译
- 排除了WASI（WebAssembly系统接口）等不支持网络的环境

### 2. 核心函数 `lookup_host`
```rust
pub async fn lookup_host<T>(host: T) -> io::Result<impl Iterator<Item = SocketAddr>> 
where
    T: ToSocketAddrs
```
- **功能**：执行DNS解析并返回Socket地址迭代器
- **参数**：接受任何实现`ToSocketAddrs` trait的类型（如&str）
- **异步特性**：通过`.await`实现非阻塞DNS查询
- **返回值**：成功时返回SocketAddr迭代器，失败时返回`io::Error`

### 3. 关键依赖
```rust
use crate::net::addr::{self, ToSocketAddrs};
use std::net::SocketAddr;
```
- 依赖`addr`模块的`to_socket_addrs`实现具体解析逻辑
- 使用标准库的SocketAddr类型表示网络地址

## 工作原理
1. **接口调用**：用户通过`net::lookup_host("host:port").await`发起请求
2. **参数处理**：参数类型需实现`ToSocketAddrs` trait（如字符串自动实现）
3. **异步解析**：调用`addr::to_socket_addrs`进行异步DNS查询
4. **结果返回**：返回包含所有解析结果的迭代器，允许用户逐个处理地址

## 在项目中的角色
作为Tokio网络模块的核心组件，该文件提供了异步DNS解析的基础功能，使用户能够在异步环境中安全高效地进行网络地址解析，是构建TCP/UDP客户端/服务器的基础支持模块。
