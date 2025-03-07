这个文件定义了一个名为 `AnyDelimiterCodec` 的结构体，它实现了 `Decoder` 和 `Encoder` trait，用于根据给定的分隔符将数据分割成块。

**主要组成部分：**

*   **`AnyDelimiterCodec` 结构体：**
    *   `next_index`:  一个优化搜索的索引，记录下一个需要检查分隔符的位置。
    *   `max_length`:  一个可选的最大块长度。如果设置了，超过此长度的块将被丢弃。
    *   `is_discarding`:  一个标志，指示当前是否正在丢弃超过最大长度的块。
    *   `seek_delimiters`:  用于解码时搜索的分隔符列表（`Vec<u8>`）。
    *   `sequence_writer`:  用于编码时写入的序列（`Vec<u8>`），通常用作块之间的分隔符。
*   **`new` 和 `new_with_max_length` 方法：**
    *   `new`:  创建一个 `AnyDelimiterCodec` 实例，使用给定的分隔符和序列写入器，没有最大长度限制。
    *   `new_with_max_length`:  创建一个 `AnyDelimiterCodec` 实例，并设置最大块长度。设置最大长度对于防止潜在的安全风险非常重要。
*   **`max_length` 方法：**  返回解码时的最大块长度。
*   **`Decoder` trait 的实现：**
    *   `decode`:  尝试从给定的 `BytesMut` 缓冲区中解码一个块。它会搜索 `seek_delimiters` 中的任何字符。如果找到分隔符，则返回一个 `Bytes` 类型的块。如果达到最大长度限制，则返回错误。如果到达缓冲区的末尾但未找到分隔符，则返回 `None`。
    *   `decode_eof`:  在输入结束时尝试解码剩余的数据。如果缓冲区中还有数据，则返回剩余的数据作为一个块。
*   **`Encoder` trait 的实现：**
    *   `encode`:  将给定的数据块编码到 `BytesMut` 缓冲区中，并在块的末尾添加 `sequence_writer`。
*   **`Default` trait 的实现：**  提供一个默认的 `AnyDelimiterCodec` 实例，使用默认的分隔符和序列写入器。
*   **`AnyDelimiterCodecError` 枚举：**  定义了可能发生的错误，包括 `MaxChunkLengthExceeded` 和 `Io` 错误。
*   **`fmt::Display` 和 `From<io::Error>` trait 的实现：**  用于错误处理和格式化。

**功能：**

该文件提供了一个通用的编解码器，可以根据用户定义的分隔符将数据流分割成块，并使用另一个分隔符将块重新组合。它支持设置最大块长度以防止潜在的拒绝服务攻击。

**与其他文件的关系：**

*   使用 `crate::codec::decoder::Decoder` 和 `crate::codec::encoder::Encoder` trait，定义了编解码器的接口。
*   使用 `bytes` crate 中的 `Bytes` 和 `BytesMut` 类型来处理字节数据。
*   定义了 `AnyDelimiterCodecError` 用于处理编解码过程中可能发生的错误。
