# Live Integrated OAL Production-Cycle Verification

**Date:** 2026-08-14  
**Project:** CaseMetrology  
**Status:** PASS — engineering/prevalidation verification, not formal validation data

## Objective

Verify that a live camera acquisition can be processed through the complete
CaseMetrology OAL workflow without changing the frozen measurement pipeline.

The verified sequence was:

1. controlled live image acquisition;
2. frozen blank-reference segmentation;
3. frozen PCA OAL pixel measurement;
4. spatial/directional calibration;
5. persistent annotated PNG generation;
6. persistent JSON measurement record generation;
7. durable SQLite outbox registration;
8. automatic HTTP transfer over Tailscale;
9. remote SHA-256 verification and durable storage on the office computer;
10. verified receiver acknowledgement; and
11. local outbox transition from pending to delivered.

## Camera State

Locked research camera controls were applied and verified before acquisition.

- Device: `/dev/case-metrology-camera`
- Resolution: 1456 x 1088
- Reported frame rate: 44.00 fps
- Git commit at acquisition: `38d14b145492299c7f756002423168d573b778d9`
- Git working tree dirty: False

## Blank Reference

Session:

`oal_live_blank_20260814_20260814_165722`

Image:

`raw_images/acquisition/oal_live_blank_20260814_20260814_165722/oal_live_blank_20260814_20260814_165724_840872_01.png`

The installed final fixture remained in place. No cartridge case was present
during blank-reference acquisition.

## Live Specimen

Part ID: `146`

Session:

`oal_live_case_146_20260814_20260814_165947`

Image:

`raw_images/acquisition/oal_live_case_146_20260814_20260814_165947/oal_live_case_146_20260814_20260814_165949_918910_01.png`

## Measurement Result

- Pipeline passed: True
- OAL: `0.991440910 in`
- OAL pixels: `518.796736284 px`
- Effective scale: `523.275498385 px/in`
- PCA axis angle: `88.145075 deg`

## Persistent Local Artifacts

JSON record:

`/home/timmy/.local/share/casemetrology/artifacts/2026-08-14/records/live_case_146_20260814_165949.json`

Annotated PNG:

`/home/timmy/.local/share/casemetrology/artifacts/2026-08-14/annotated/live_case_146_20260814_165949_annotated.png`

## Transport Result

- Outbox status: `delivered`
- Delivery attempts: `1`
- Delivery success: `True`
- HTTP status: `201`
- Receiver status: `stored`
- Delivery error: `None`

The receiver verifies the annotated-image SHA-256 before durable storage and
returns the verified hash in its acknowledgement. The Nano marks the outbox
entry delivered only after validating that acknowledgement.

## Interpretation

This test demonstrates successful integration of live controlled acquisition,
the frozen OAL measurement pipeline, persistent local evidence generation,
durable retry-safe queueing, and verified remote storage.

This was an engineering/prevalidation verification and is not part of the
formal OAL validation dataset.

No conclusion regarding system accuracy or repeatability should be drawn from
this single live cycle.

## Result

**PASS**

The complete live CaseMetrology OAL production-style workflow operated
successfully from controlled camera acquisition through verified remote
storage without modifying the frozen PCA measurement result.
