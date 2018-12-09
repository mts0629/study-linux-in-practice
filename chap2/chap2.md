続き。

[http://soratobi96.hatenablog.com/entry/20181201/1543672068:embed:cite]

### 第2章 ユーザモードで実現する機能

### システムコール

ユーザモードのプロセスは、それ自身のコードやライブラリを介してシステムコールを呼び出し、次のようなOSの機能を利用する。

- プロセス生成/削除
- メモリ確保/開放
- プロセス間通信
- ネットワーク
- ファイルシステム操作
- ファイル操作、デバイスアクセス

システムコールが呼び出されると割り込みが発生し、CPUは一時的にカーネルモードに遷移する。

カーネルはプロセスの要求（ハードウェアリソースを確保する量など）をチェックし、それが妥当であるときのみシステムコールを実行する。

#### `strace`

プロセスの発行するシステムコール呼び出しを`strace`で確認できる。

次のhello worldプログラムを確認すると、28回のシステムコールが発行されており、そのほとんどは`main()`の前後に実行されるものである（文字列を出力するのは`write(1, "hello world\n", 12)`）。

```c
#include <stdio.h>

int main(void)
{
    puts("hello world");

    return 0;
}
```

```sh
$ gcc -o hello hello.c
$ strace -o hello.log ./hello
$ cat hello.log
execve("./hello", ["./hello"], 0x7ffd8f809040 /* 55 vars */) = 0
brk(NULL)                               = 0x55ea759b6000
access("/etc/ld.so.nohwcap", F_OK)      = -1 ENOENT (No such file or directory)
access("/etc/ld.so.preload", R_OK)      = -1 ENOENT (No such file or directory)
openat(AT_FDCWD, "/etc/ld.so.cache", O_RDONLY|O_CLOEXEC) = 3
...
fstat(1, {st_mode=S_IFCHR|0620, st_rdev=makedev(136, 1), ...}) = 0
brk(NULL)                               = 0x55ea759b6000
brk(0x55ea759d7000)                     = 0x55ea759d7000
write(1, "hello world\n", 12)           = 12
exit_group(0)                           = ?
+++ exited with 0 +++
```

言語にかかわらず、カーネルに処理を依頼するときは最終的にシステムコールが発行される。

Pythonで同様のプログラムを実行すると、781回のシステムコールが発行されている。

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

print("hello world")
```

```sh
$ strace -o hello_py.log python3 ./hello.py
hello world
$ cat hello_py.log
execve("/usr/bin/python3", ["python3", "./hello.py"], 0x7ffc7a46d748 /* 58 vars */) = 0
brk(NULL)                               = 0x2971000
access("/etc/ld.so.nohwcap", F_OK)      = -1 ENOENT (No such file or directory)
...
write(1, "hello world\n", 12)           = 12
...
sigaltstack(NULL, {ss_sp=0x298f810, ss_flags=0, ss_size=8192}) = 0
sigaltstack({ss_sp=NULL, ss_flags=SS_DISABLE, ss_size=0}, NULL) = 0
exit_group(0)                           = ?
+++ exited with 0 +++
```

#### `sar`

現在CPUが行っている処理の種類と内訳は、`sar` (System Admin Reporter) コマンドで確認できる。

次では、`sar -P ALL 1`で各CPUコア（実行環境は4コア）の利用率内訳とその平均値を1秒ごとに取得し、`<ctrl+C>`で中断した時点までの平均値を出力している。

```sh
$ sar -P ALL 1
Linux 4.15.0-39-generic (***)       12/01/2018      _x86_64_        (4 CPU)

06:13:09 PM     CPU     %user     %nice   %system   %iowait    %steal     %idle
06:13:10 PM     all      9.98      0.00      3.24      0.00      0.00     86.78
06:13:10 PM       0      6.93      0.00      2.97      0.00      0.00     90.10
06:13:10 PM       1     16.00      0.00      3.00      0.00      0.00     81.00
06:13:10 PM       2      7.00      0.00      2.00      0.00      0.00     91.00
06:13:10 PM       3     11.11      0.00      3.03      0.00      0.00     85.86
...
^C


Average:        CPU     %user     %nice   %system   %iowait    %steal     %idle
Average:        all      6.11      0.00      1.45      0.05      0.00     92.39
Average:          0      4.48      0.00      1.89      0.00      0.00     93.63
Average:          1      4.31      0.00      1.10      0.00      0.00     94.58
Average:          2      5.40      0.00      1.20      0.10      0.00     93.30
Average:          3     10.13      0.00      1.49      0.20      0.00     88.18
```

#### CPUモードと使用率

`sar`の出力から確認できる、各CPUモードのプロセッサ使用率は次の値となる。

- ユーザモード: `%user` + `%nice`
- カーネルモード: `%system`

親プロセスのIDを取得するシステムコール`getppid()`を無限ループするプログラムについて、バックグラウンドで実行し、CPU使用率を確認する。

```c
#include <sys/types.h>
#include <unistd.h>

int main(void)
{
    for (;;) {
        getppid();
    }
}
```

```sh
$ gcc -o ppidloop ppidloop.c
$ ./ppidloop &
[1] 8232
$ sar -P ALL 1 1
Linux 4.15.0-39-generic (***)       12/01/2018      _x86_64_        (4 CPU)
...

Average:        CPU     %user     %nice   %system   %iowait    %steal     %idle
Average:        all     11.47      0.00     17.21      0.00      0.00     71.32
Average:          0      1.00      0.00      1.00      0.00      0.00     98.00
Average:          1      8.08      0.00      0.00      0.00      0.00     91.92
Average:          2     34.00      0.00     66.00      0.00      0.00      0.00
Average:          3      3.96      0.00      0.00      0.00      0.00     96.04
$ kill 8232
```

CPU2でプログラムが実行されており、ユーザ処理使用率（ループ処理）が34%、システム使用率（システムコール処理）が66%となっている。

#### 所要時間の確認

`strace -T`でシステムコールの処理にかかった所要時間を[us]制度で取得できる。

```sh
$ strace -T -o hello.log ./hello
hello world
$ cat hello.log
execve("./hello", ["./hello"], 0x7ffe38853468 /* 58 vars */) = 0 <0.000565>
brk(NULL)                               = 0x564aa7e4d000 <0.000523>
...
brk(0x564aa7e6e000)                     = 0x564aa7e6e000 <0.000018>
write(1, "hello world\n", 12)           = 12 <0.000020>
exit_group(0)                           = ?
+++ exited with 0 +++
```

ここでは、`write()`の処理に20[us]かかっている。

#### ラッパー関数

システムコールはアーキテクチャに依存するアセンブリコードで呼び出す必要がある。一例として、x-86_64アーキテクチャでの`getppid()`呼び出しは次のアセンブリコードとなる（GNU Assembler表記）。

```asm
mov $0x6e, %eax
syscall
```

OSは、高級言語で使用するためのシステムコールを呼び出すラッパー関数を提供している（このAPI自体もシステムコールと呼ばれる）。

#### 標準Cライブラリ

Linuxで使用される標準Cライブラリは多くの場合GNU実装のglibcで、システムコールのラッパー関数およびPOSIX (Portable operating system interface) 準拠の関数を提供している。

プログラムがリンクしている共有ライブラリは`ldd`で確認できる。

```sh
$ ldd ppidloop
        linux-vdso.so.1 (0x00007fffd67e5000)
        libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007f877a539000)
        /lib64/ld-linux-x86-64.so.2 (0x00007f877ab2c000)
```

上記の`getppid()`を無限ループするプログラムでは、3種のライブラリがリンクされている。

- linux-vdso.so.1: Linux Virtual Dynamic Shared Object。システムコールをユーザー空間で処理させて高速化を図るライブラリらしい
- libc.so.6: 標準Cライブラリ
- ld-linux-x86-64.so.2: 動的リンカ