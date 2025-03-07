# 代码文件解释：`tinyhttp.rs`

## 目的  
该文件是一个基于 Tokio 的极简 HTTP 服务器示例，用于演示如何通过 Tokio 的异步 IO 原语手动实现 HTTP 请求/响应处理。它不依赖任何大型 HTTP 库（如 Hyper），而是通过底层操作展示协议实现的核心逻辑，适合学习 Tokio 的异步编程模型和 HTTP 协议基础。

---

## 核心组件与功能

### 1. **主函数 (`main`)**  
- **功能**：绑定 TCP 端口并启动服务器。  
- **流程**：  
  1. 从命令行参数获取监听地址（默认 `127.0.0.1:8080`）。  
  2. 使用 `TcpListener` 监听指定地址。  
  3. 循环接受新连接，为每个连接创建异步任务（通过 `tokio::spawn`）进行处理。  

```rust
#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    let addr = ...;
    let server = TcpListener::bind(&addr).await?;
    loop {
        let (stream, _) = server.accept().await?;
        tokio::spawn(process(stream));
    }
}
```

---

### 2. **连接处理 (`process` 函数)**  
- **功能**：处理单个 TCP 连接的 HTTP 请求与响应。  
- **流程**：  
  1. 使用 `Framed` 将 TCP 流包装为基于 `Http` 编解码器的流（`Framed<_, Http>`）。  
  2. 循环读取请求，调用 `respond` 生成响应，并通过 `send` 发送响应。  
  3. 错误处理：捕获异常并打印错误信息。  

```rust
async fn process(stream: TcpStream) -> Result<(), Box<dyn Error>> {
    let mut transport = Framed::new(stream, Http);
    while let Some(request) = transport.next().await {
        if let Ok(req) = request {
            let response = respond(req).await?;
            transport.send(response).await?;
        }
    }
    Ok(())
}
```

---

### 3. **响应生成 (`respond` 函数)**  
- **功能**：根据请求路径生成对应的 HTTP 响应。  
- **路由逻辑**：  
  - `/plaintext`：返回纯文本 `"Hello, World!"`，Content-Type 为 `text/plain`。  
  - `/json`：返回 JSON 对象 `{ "message": "Hello, World!" }`，Content-Type 为 `application/json`。  
  - 其他路径：返回 404 错误。  

```rust
async fn respond(req: Request<()>) -> Result<Response<String>, Box<dyn Error>> {
    let body = match req.uri().path() {
        "/plaintext" => "Hello, World!".to_string(),
        "/json" => serde_json::to_string(&Message { message: "Hello, World!" })?,
        _ => String::new(),
    };
    let response = Response::builder()
        .status(if body.is_empty() { StatusCode::NOT_FOUND } else { StatusCode::OK })
        .header("Content-Type", ...)
        .body(body)?;
    Ok(response)
}
```

---

### 4. **HTTP 编解码器 (`Http` 结构体)**  
- **功能**：实现 HTTP/1.1 协议的编码（响应生成）和解码（请求解析）。  
- **编码 (`Encoder` trait)**：  
  - 将 `Response<String>` 转换为字节流，包含 HTTP 头（如 `Content-Length`、`Date`）和正文。  
  - 使用自定义 `BytesWrite` 结构体优化字符串拼接性能。  

```rust
impl Encoder<Response<String>> for Http {
    fn encode(&mut self, item: Response<String>, dst: &mut BytesMut) -> io::Result<()> {
        // 手动构造 HTTP 响应头和正文
        write!(
            BytesWrite(dst),
            "HTTP/1.1 {}...\r\n...",
            item.status()
        );
        // ...
    }
}
```

- **解码 (`Decoder` trait)**：  
  - 使用 `httparse` 解析接收到的字节流为 `Request` 对象。  
  - 处理 HTTP 方法、路径、版本及头部字段。  

```rust
impl Decoder for Http {
    fn decode(&mut self, src: &mut BytesMut) -> io::Result<Option<Request<()>>> {
        let mut parsed = httparse::Request::new(&mut [httparse::EMPTY_HEADER; 16]);
        let status = parsed.parse(src.as_ref())?;
        // 解析方法、路径、头部等，构造 Request 对象
    }
}
```

---

### 5. **日期优化 (`date` 模块)**  
- **功能**：高效生成 HTTP `Date` 头的值。  
- **优化点**：  
  - 避免频繁格式化系统时间，通过缓存最近生成的日期字符串减少计算开销。  
  - 使用 `thread_local` 存储缓存，仅在时间变化时重新生成。  

```rust
pub struct Now(());
impl fmt::Display for Now {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        // 通过缓存优化 Date 头的生成
        LAST.with(|cache| { ... })
    }
}
```

---

## 项目中的角色  