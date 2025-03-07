# 文件说明：Tokio 运行时 IO 驱动指标收集模块

## 文件目的
该文件实现了 Tokio 运行时中与 IO 驱动相关的性能指标收集功能。通过原子计数器记录文件描述符注册/注销次数及 IO 事件准备次数，为运行时监控和性能调优提供数据支持。

## 关键组件
### 1. IoDriverMetrics 结构体
```rust
pub(crate) struct IoDriverMetrics {
    pub(super) fd_registered_count: MetricAtomicU64,
    pub(super) fd_deregistered_count: MetricAtomicU64,
    pub(super) ready_count: MetricAtomicU64,
}
```
- **字段说明**：
  - `fd_registered_count`：已注册的文件描述符总数
  - `fd_deregistered_count`：已注销的文件描述符总数
  - `ready_count`：准备就绪的 IO 事件总数

### 2. 方法实现
```rust
impl IoDriverMetrics {
    // 增加注册计数
    pub(crate) fn incr_fd_count(&self) {
        self.fd_registered_count.add(1, Relaxed);
    }

    // 增加注销计数
    pub(crate) fn dec_fd_count(&self) {
        self.fd_deregistered_count.add(1, Relaxed);
    }

    // 按指定值增加就绪计数
    pub(crate) fn incr_ready_count_by(&self, amt: u64) {
        self.ready_count.add(amt, Relaxed);
    }
}
```
- 使用原子操作（Relaxed 内存序）保证多线程环境下的安全计数
- 通过无锁的原子操作实现高性能指标收集

## 条件编译处理
```rust
#![cfg_attr(not(feature = "net"), allow(dead_code))]
```
- 当未启用 `net` 功能时：
  - 允许代码未被使用时不报错
  - 通过条件编译禁用度量功能以减少运行时开销

## 在项目中的角色