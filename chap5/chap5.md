# 5章 メモリ管理

Linuxは、システムに搭載されるメモリをカーネルのメモリ管理システムにより管理する。

## 統計情報

`free`コマンドによりメモリの統計情報を確認できる。

```
$ free
              total        used        free      shared  buff/cache   available
Mem:        8068456     2340640     4030844      315076     1696972     5178248
Swap:       2097148           0     2097148
```

- `total`: システムに搭載される全メモリ量
- `free`: 見かけ上の空きメモリ
- `buff/cache`: バッファキャッシュ、ページキャッシュが使用するメモリ。システムの空きメモリが減少してきた際に開放される
- `available`: 実質的な空きメモリ。freeフィールドのメモリ量+開放できるカーネル内メモリ領域のサイズ

`sar -r [sec]` で確認できるリアルタイム統計情報と一部対応している。

- `free` - `kbmemfree`
- `buff/cache`- `kbbuffers` + `kbcached`

```
$ sar -r 1
...

23時55分16秒 kbmemfree   kbavail kbmemused  %memused kbbuffers  kbcached  kbcommit   %commit  kbactive   kbinact   kbdirty
23時55分17秒   3998384   5148496   4070072     50.44     93112   1529620   8040504     79.10   2581208   1147640       172
23時55分18秒   3997920   5148032   4070536     50.45     93112   1530024   8040504     79.10   2581264   1148044       172
23時55分19秒   3997796   5147908   4070660     50.45     93112   1530116   8040504     79.10   2581340   1148152       172
23時55分20秒   3997300   5147416   4071156     50.46     93120   1530528   8040504     79.10   2581404   1148564       196
...
```

## Out Of Memory

メモリ使用量の増加に伴ってメモリ管理システムはカーネル内の開放可能なメモリ領域を開放するが、領域を使い果たすとOut Of Memory (OOM) 状態となる。

この場合カーネルはOOM killer機能により、適当なプロセスを強制終了 (kill) しメモリ領域を開放することでシステムの停止を防ぐ。

OOM Killerの優先度を設定でき、強制終了を防ぐことができる。