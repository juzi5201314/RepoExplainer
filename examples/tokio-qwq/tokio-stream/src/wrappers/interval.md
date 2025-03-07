# IntervalStream 模块说明

## 概述
IntervalStream 是 Tokio 流库中用于包装 Tokio 定时器（Interval）的适配器结构体，实现了标准流（Stream）trait，使得定时器可以无缝集成到异步流处理框架中。

## 核心组件

### 结构体定义
```rust
pub struct IntervalStream {
    inner: Interval,
}
```
- **inner**：封装 Tokio 的 Interval 定时器实例，负责定时触发事件

### 关键方法
1. **构造方法**
```rust
pub fn new(interval: Interval) -> Self
```
- 通过传入 Tokio 的 Interval 实例创建 IntervalStream 对象

2. **资源释放**
```rust
pub fn into_inner(self) -> Interval
```
- 将 IntervalStream 转换回原始 Interval 对象，释放内部资源

### Stream Trait 实现
```rust
impl Stream for IntervalStream {
    type Item = Instant;

    fn poll_next(...) -> Poll<Option<Instant>> {
        self.inner.poll_tick(cx).map(Some)
    }

    fn size_hint(...) -> (usize, Option<usize>) {
        (usize::MAX, None)
    }
}
```
- **poll_next**：通过 Interval 的 poll_tick 方法获取下一个时间点，返回 Some(Instant)
- **size_hint**：声明这是一个无限流（无限次数触发）

### 辅助 Trait 实现
```rust
impl AsRef<Interval> for IntervalStream { ... }
impl AsMut<Interval> for IntervalStream { ... }
```
- 提供对内部 Interval 的安全引用访问，支持在不取出对象的情况下进行配置修改

## 工作原理
1. **包装机制**：将 Tokio 的 Interval 封装为符合 Stream 标准的异步流
2. **事件触发**：每次 poll_next 调用会轮询定时器的下一个触发时间点
3. **无限流特性**：通过 size_hint 明确标识流不会自然结束

## 使用场景
- 定时任务调度（如每秒执行一次）
- 心跳包发送
- 数据轮询
- 与流处理操作符（如 map、filter）组合使用

## 示例代码
```rust
let interval = interval(Duration::from_millis(100));
let mut stream = IntervalStream::new(interval);
while let Some(instant) = stream.next().await {
    // 处理定时事件
}
```

## 项目中的角色