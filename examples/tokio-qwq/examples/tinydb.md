# `tinydb.rs` 文件详解

## 文件目的
该文件是一个基于 Tokio 的简单键值对数据库服务器示例，演示如何在多个客户端之间共享状态。支持通过 `GET` 和 `SET` 命令操作内存中的键值对数据库，并通过基于行的文本协议与客户端通信。

---

## 核心组件

### 1. **数据库结构 (`Database` 结构体)**
```rust
struct Database {
    map: Mutex<HashMap<String, String>>,
}
```
- **功能**：存储键值对的内存数据库。
- **线程安全**：通过 `Mutex` 实现对 `HashMap` 的独占访问，确保多线程并发操作的安全性。
- **共享机制**：使用 `Arc<Database>` 在所有客户端间共享数据库实例。

---

### 2. **请求与响应枚举**
#### 请求 (`Request` enum)
```rust
enum Request {
    Get { key: String },
    Set { key: String, value: String },
}
```
- **GET 请求**：获取指定键的值。
- **SET 请求**：设置键值对，返回旧值（如果存在）。
- **解析方法**：`parse` 方法通过拆分输入字符串解析命令。

#### 响应 (`Response` enum)
```rust
enum Response {
    Value { key: String, value: String },
    Set { key: String, value: String, previous: Option<String> },
    Error { msg: String },
}
```
- **响应格式化**：通过 `serialize` 方法将响应转换为字符串，例如：
  - `GET` 成功返回 `key = value`。
  - `SET` 返回设置结果及旧值。
  - 错误返回 `error: message`。

---

### 3. **服务器逻辑 (`main` 函数)**
```rust
#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    // 监听地址解析与初始化
    let addr = env::args().nth(1).unwrap_or_else(|| "127.0.0.1:8080".to_string());
    let listener = TcpListener::bind(&addr).await?;
    
    // 初始化数据库（初始键值对 "foo" → "bar"）
    let db = Arc::new(Database { map: Mutex::new({
        let mut m = HashMap::new();
        m.insert("foo".to_string(), "bar".to_string());
        m
    })});
    
    // 处理连接循环
    loop {
        let (socket, _) = listener.accept().await?;
        let db_clone = db.clone();
        tokio::spawn(handle_connection(socket, db_clone));
    }
}
```
- **连接处理**：为每个新连接启动异步任务，通过 `Arc` 克隆数据库引用。
- **协议处理**：使用 `Framed` 和 `LinesCodec` 将 TCP 流转换为行协议，逐行解析客户端输入。

---

### 4. **请求处理 (`handle_request` 函数)**
```rust
fn handle_request(line: &str, db: &Arc<Database>) -> Response {
    let request = Request::parse(line).unwrap_or_else(|e| return Response::Error { msg: e });
    
    let mut map = db.map.lock().unwrap();
    match request {
        Request::Get { key } => {
            match map.get(&key) {
                Some(v) => Response::Value { key, value: v.clone() },
                None => Response::Error { msg: format!("no key {key}") },
            }
        },
        Request::Set { key, value } => {
            let prev = map.insert(key.clone(), value.clone());
            Response::Set { key, value, previous: prev }
        }
    }
}
```
- **线程安全操作**：通过 `Mutex` 锁获取数据库的可变引用。
- **命令执行**：
  - `GET`：直接从 `HashMap` 获取值。
  - `SET`：插入键值对并返回旧值。

---

### 5. **客户端通信处理**
```rust
// 在异步任务中处理客户端连接
async fn handle_connection(socket: TcpStream, db: Arc<Database>) {
    let mut lines = Framed::new(socket, LinesCodec::new());
    
    while let Some(result) = lines.next().await {
        match result {
            Ok(line) => {
                let response = handle_request(&line, &db);
                let msg = response.serialize();
                if let Err(e) = lines.send(msg.as_str()).await {
                    eprintln!("发送响应失败: {e}");
                }
            },
            Err(e) => eprintln!("解码失败: {e}"),
        }
    }
}
```
- **协议解析**：逐行读取客户端输入，调用 `handle_request` 处理。
- **响应发送**：将响应字符串通过 TCP 连接返回客户端。

---

## 项目中的角色