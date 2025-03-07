rust
use std::fmt;

#[derive(Clone, Copy, PartialEq)]
pub(crate) struct Pack {
    mask: usize,
    shift: u32,
}

impl Pack {
    // 创建将值存放在最低有效位的Pack实例
    pub(crate) const fn least_significant(width: u32) -> Pack {
        let mask = mask_for(width);
        Pack { mask, shift: 0 }
    }

    // 在当前Pack之后添加新字段
    pub(crate) const fn then(&self, width: u32) -> Pack {
        let shift = (usize::BITS - self.mask.leading_zeros()) as u32;
        let mask = mask_for(width) << shift;
        Pack { mask, shift }
    }

    // 获取当前字段占用的位数
    pub(crate) const fn width(&self) -> u32 {
        usize::BITS as u32 - ((self.mask >> self.shift).leading_zeros())
    }

    // 计算可表示的最大值
    pub(crate) const fn max_value(&self) -> usize {
        (1 << self.width()) - 1
    }

    // 将值打包到基础值中
    pub(crate) fn pack(&self, value: usize, base: usize) -> usize {
        assert!(value <= self.max_value());
        (base & !self.mask) | (value << self.shift)
    }

    // 从基础值中解包值
    pub(crate) fn unpack(&self, src: usize) -> usize {
        unpack(src, self.mask, self.shift)
    }
}

impl fmt::Debug for Pack {
    fn fmt(&self, fmt: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(fmt, "Pack {{ mask: {:b}, shift: {} }}", self.mask, self.shift)
    }
}

// 生成n位全1掩码
pub(crate) const fn mask_for(n: u32) -> usize {
    let shift = 1usize.wrapping_shl(n - 1);
    shift | (shift - 1)
}

// 通过掩码和位移解包值
pub(crate) const fn unpack(src: usize, mask: usize, shift: u32) -> usize {
    (src & mask) >> shift
}
```

### 代码文件解释

#### **目的**
该文件提供了一套位域操作工具，用于在单个 `usize` 整数中紧凑存储多个数值字段。通过位掩码和位移操作，实现高效内存管理和快速访问，适用于需要高性能的场景（如 Tokio 异步运行时的状态管理）。

---

#### **关键组件**

1. **`Pack` 结构体**
   - **字段**：
     - `mask`: 位掩码，用于标记字段占用的位范围。
     - `shift`: 位移量，表示字段在整数中的起始位置。
   - **功能**：定义如何将数值打包到 `usize` 中或从中解包。

2. **构造方法**
   - **`least_significant(width)`**：
     - 创建将值存放在最低有效位的 `Pack` 实例。
     - 示例：`width=3` 生成 `mask=0b111`，`shift=0`。
   - **`then(width)`**：
     - 在当前字段之后添加新字段，自动计算新位移和掩码。
     - 示例：若当前字段占用了前 4 位，则新字段从第 5 位开始。

3. **属性方法**
   - **`width()`**：返回字段占用的位数。
   - **`max_value()`**：计算字段可表示的最大值（`2^width - 1`）。

4. **操作方法**
   - **`pack(value, base)`**：
     - 将 `value` 按位掩码和位移合并到 `base` 值中。
     - 示例：`base=0b1010`, `mask=0b11`, `shift=2` → `0b1010 & ~0b11 = 0b1000`，加上 `value << shift`。
   - **`unpack(src)`**：
     - 从 `src` 中提取字段值，通过位与和右移操作。

5. **辅助函数**
   - **`mask_for(n)`**：生成 `n` 位全 1 的掩码（如 `n=3` → `0b111`）。
   - **`unpack()`**：静态解包函数，供 `Pack` 方法调用。

---

#### **实现细节**
- **位掩码计算**：
  - `mask_for(n)` 使用位移操作高效生成掩码，避免循环。
  - `then()` 通过 `leading_zeros` 计算当前字段结束位置，确保新字段不重叠。
- **安全性**：
  - `pack()` 包含断言，确保值不超过最大值，防止溢出。

---

#### **项目中的角色**
该文件为 Tokio 的底层状态管理提供位域操作工具，通过紧凑的 `usize` 存储多个字段，优化内存使用和访问速度，是高性能异步运行时基础设施的重要组成部分。
