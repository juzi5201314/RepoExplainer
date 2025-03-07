# 文件说明：`tokio/src/macros/cfg.rs`

## **目的**  
该文件定义了一系列条件编译宏，用于管理Tokio库中不同功能模块的编译条件和文档配置。通过这些宏，Tokio能够根据编译时的特性开关、目标平台、不稳定功能等条件，灵活控制代码的编译范围，并确保文档中正确标注配置要求。

---

## **关键组件**

### **1. 基础条件宏**
- **`feature!`**  
  处理特性开关的通用宏，自动添加`#[cfg(...)]`和文档注解`doc(cfg(...))`，确保代码和文档同步。  
  示例：  
  ```rust
  #![feature(some_feature)]
  // → 编译时启用该特性，并在文档中标记需要该特性。

- **平台相关宏**  
  - `cfg_windows`/`cfg_unix`：启用特定于Windows/Unix的代码，同时在文档中注明平台要求。  
  - `cfg_unstable_windows`：针对Windows的不稳定功能，需同时满足`tokio_unstable`和Windows平台。

### **2. 模块化功能控制**
- **功能特性宏**  
  根据启用的Cargo特性控制代码编译：  
  - `cfg_net`：网络功能（需`feature = "net"`）。  
  - `cfg_io_std`：标准IO功能（需`feature = "io-std"`）。  
  - `cfg_time`：时间功能（需`feature = "time"`）。  
  - `cfg_test_util`：测试工具（需`feature = "test-util"`）。  

- **组合条件宏**  
  处理复杂依赖关系：  
  - `cfg_io_driver`：需`net`或Unix平台的`process`/`signal`特性。  
  - `cfg_block_on`：需`fs`、`net`、`io-std`或`rt`特性中的至少一个。  

### **3. 平台与架构适配**
- **平台特化宏**  
  - `cfg_net_unix`：Unix平台且启用`net`特性。  
  - `cfg_net_windows`：Windows平台且启用`net`特性。  
  - `cfg_64bit_metrics`：要求目标平台支持64位原子操作（如`target_has_atomic = "64"`）。  

- **排除条件宏**  
  通过`cfg_not_`前缀宏排除特定条件，例如：  
  - `cfg_not_io_util`：当未启用`io-util`特性时生效。  

### **4. 测试与调试支持**
- **测试环境宏**  
  - `cfg_loom`：用于并发测试框架Loom的条件编译。  
  - `cfg_taskdump`：针对Linux平台的实验性任务转储功能（需`tokio_unstable`和特定架构）。  

---

## **作用于项目**
该文件是Tokio项目的**条件编译核心**，通过定义标准化的宏简化代码中的条件逻辑，确保不同功能模块在正确配置下编译，并自动生成准确的文档配置说明。它帮助Tokio实现高度模块化和跨平台兼容性，同时维护代码的清晰性和可维护性。
