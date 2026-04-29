# 阶段 08：段 2 视频提交

> 工具：Seedance 2.0
> ⚠️ 段 2 的 prompt 在阶段 07 已审核通过。本阶段仅提交，不重新组装 prompt。

## 前置条件

- 阶段 07 已审核通过
- 段 1 视频已完成
- `05-videos/ep01/lastframe_seg1.png` 存在

## 流程

从 `05-videos/ep01/assets.md` 读取段 2 的 prompt 和参数，直接提交。

```bash
python3 <video-gen>/scripts/seedance.py create \
  --prompt "{阶段07审核通过的段2 prompt}" \
  --ref-images ... \
  --audio ... \
  --ratio 9:16 --duration 15 --generate-audio true --return-last-frame true
```

## 完成后

→ `stages/09-video-seg3.md`
