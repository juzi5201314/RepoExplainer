# MockOpenOptions 模块说明

## 概述
该文件是 Tokio 异步文件系统模块的测试辅助组件，提供 `std::fs::OpenOptions` 的模拟实现。通过 mockall 库生成可控制的模拟对象，用于在单元测试中隔离文件系统操作。

## 核心组件
### 1. 模拟结构体定义
```rust
mock! {
    pub OpenOptions { ... }
}
```
- 使用 mockall 宏生成 MockOpenOptions 结构体，模拟标准库的 OpenOptions 行为
- 提供与标准库一致的接口方法：
  - 文件操作模式配置方法（append/create/truncate等）
  - 核心 open 方法返回 MockFile（模拟文件对象）
  - 支持 Clone 特性

### 2. 平台相关扩展
```rust
#[cfg(unix)] impl OpenOptionsExt { ... }
#[cfg(windows)] impl OpenOptionsExt { ... }
```
- 实现不同操作系统的扩展 trait：
  - Unix：自定义标志位和权限模式设置
  - Windows：访问模式、共享模式等Windows特有配置

## 工作原理
1. **测试环境切换**  
   项目通过条件编译在测试时使用该模拟实现，正常运行时使用标准库版本：
   ```rust
   #[cfg(test)] use mock_open_options::MockOpenOptions as StdOpenOptions
   #[cfg(not(test))] use std::fs::OpenOptions as StdOpenOptions
   ```

2. **模拟对象特性**  
   - 允许在测试中预设 open 方法的返回值（成功/失败）
   - 可控制文件操作模式配置的验证逻辑
   - 独立于真实文件系统状态，提升测试稳定性

3. **异步集成**  
   作为 Tokio 异步文件操作的基础，该模拟实现确保异步文件操作测试的可行性，例如：
   ```rust
   // 示例测试场景
   let mut mock = MockOpenOptions::new();
   mock.expect_open()
      .returning(|_| Ok(MockFile::new()));
   ```

## 项目角色