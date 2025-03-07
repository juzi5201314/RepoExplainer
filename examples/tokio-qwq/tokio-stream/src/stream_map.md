### 文件说明：`stream_map.rs`

#### 功能与目的  
`StreamMap` 是 Tokio 流框架中的核心组件，用于合并多个异步流（Stream），并为每个流分配唯一键（Key）。它允许在迭代过程中动态插入或移除流，并追踪每个值的来源流。相比 `StreamExt::merge`，它提供了更灵活的操作模式，适用于需要动态管理流的场景（如聊天室订阅、事件驱动系统等）。

---

#### 核心组件与实现细节  

1. **结构定义**  
   ```rust
   pub struct StreamMap<K, V> {
       entries: Vec<(K, V)>,
   }
   ```
   - 使用 `Vec<(K, V)>` 存储键值对，键 `K` 必须实现 `Hash + Eq`，流 `V` 必须是 `Unpin` 类型。
   - 支持动态增删流：`insert` 插入新流，`remove` 移除指定键的流。

2. **流（Stream）实现**  
   - **`poll_next` 方法**：  
     通过 `poll_next_entry` 遍历所有流，轮询每个流的 `poll_next` 直到有值返回。  
     - **随机起始索引**：使用 `rand` 模块生成随机起始位置，避免轮询偏序。  
     - **自动清理完成流**：若流返回 `Poll::Ready(None)`，则从 `entries` 中移除。  
   - **`size_hint` 方法**：聚合所有流的 `size_hint`，返回总估计值范围。

3. **扩展功能**  
   - **批量读取**：`next_many` 和 `poll_next_many` 可一次性收集多个值到缓冲区，适用于批量处理场景。  
   - **迭代器支持**：提供 `iter`、`keys`、`values` 等方法遍历流集合。

4. **注意事项**  
   - **`Unpin` 要求**：流必须是 `Unpin` 类型，否则需通过 `pin!` 或 `Box::pin` 固定。  
   - **性能提示**：适用于“小规模”流集合（内部遍历所有条目），大规模场景建议改用 `mpsc` 通道。

---

#### 典型使用场景  

1. **动态流管理**  
   ```rust
   let mut map = StreamMap::new();
   map.insert("one", rx1); // 插入流
   map.next().await;       // 获取值并记录来源键
   map.remove("one");      // 动态移除流
   ```

2. **事件驱动系统**  
   结合 `tokio::select!` 处理命令与流事件：
   ```rust
   loop {
       tokio::select! {
           Some(cmd) = cmds.next() => { /* 处理加入/离开频道命令 */ }
           Some((chan, msg)) = channels.next() => { /* 处理频道消息 */ }
       }
   }
   ```

---

#### 在项目中的角色  