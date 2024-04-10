import json
import shutil
import uuid
from pathlib import Path

from CameraDefinition import CameraDefinition

WORKING_DIR = Path("temp/fnx-aircraft-320-better-fixed-cameras")

def main():
    if WORKING_DIR.exists():
        shutil.rmtree(WORKING_DIR)
    cfm_dir = WORKING_DIR / "SimObjects" / "Airplanes" / "FNX_320_CFM"
    iae_dir = WORKING_DIR / "SimObjects" / "Airplanes" / "FNX_320_IAE"
    cfm_dir.mkdir(parents=True, exist_ok=True)
    iae_dir.mkdir(parents=True, exist_ok=True)

    cameras_cfg = generate_cameras_cfg()
    (cfm_dir / "cameras.cfg").write_text(cameras_cfg)
    (iae_dir / "cameras.cfg").write_text(cameras_cfg)
    (WORKING_DIR / "manifest.json").write_text(generate_manifest_json())
    (WORKING_DIR / "layout.json").write_text(generate_layout_json())

    shutil.make_archive("fenix-a320-better-fixed-cameras", 'zip', "temp")
    shutil.rmtree(WORKING_DIR)

    print(f"Mod successfully built")

def generate_cameras_cfg():
    INDEX_OFFSET = 89
    str_builder = ""
    with open("cameras-template.cfg", "r") as f:
        str_builder = f.read()
    for i, cam_def in enumerate(CAM_DEFINITIONS):
        str_builder += CAM_DEF_TEMPLATE.format(
            index=INDEX_OFFSET + i,
            title=cam_def.name,
            guid=uuid.uuid4(),
            zoom=cam_def.zoom,
            xyz=cam_def.xyz,
            pbh=cam_def.pbh,
            sub_category="FixedOnPlaneIntern" if cam_def.is_cabin else "FixedOnPlaneExtern"
        )
    return str_builder

def generate_manifest_json():
    return json.dumps({
        "dependencies": [],
        "content_type": "AIRCRAFT",
        "title": "Fenix A320 - Better fixed cameras",
        "manufacturer": "Airbus",
        "creator": "mabenj",
        "package_version": "1.0.0",
        "minimum_game_version": "1.7.12",
        "release_notes": {
            "neutral": {
            "LastUpdate": "",
            "OlderHistory": ""
            }
        }
    }, indent=2)

def generate_layout_json():
    cfm_cameras_cfg = WORKING_DIR / Path("SimObjects/Airplanes/FNX_320_CFM/cameras.cfg")
    iae_cameras_cfg = WORKING_DIR / Path("SimObjects/Airplanes/FNX_320_IAE/cameras.cfg")

    cfm_size = cfm_cameras_cfg.stat().st_size
    iae_size = iae_cameras_cfg.stat().st_size
    cfm_last_write_time = cfm_cameras_cfg.stat().st_mtime_ns
    iae_last_write_time = iae_cameras_cfg.stat().st_mtime_ns

    return json.dumps({
        "content": [
            {
                "path": "SimObjects/Airplanes/FNX_320_CFM/cameras.cfg",
                "size": cfm_size,
                "date": unix_timestamp_to_windows(cfm_last_write_time)
            },
            {
                "path": "SimObjects/Airplanes/FNX_320_IAE/cameras.cfg",
                "size": iae_size,
                "date": unix_timestamp_to_windows(iae_last_write_time)
            }
        ]
    }, indent=2)

def unix_timestamp_to_windows(timestamp_ns: float):
    OFFSET = 11644473600000000000
    return timestamp_ns + OFFSET

CAM_DEFINITIONS = [
    # /images/1-tail.png
    CameraDefinition(name="Tail", zoom=1.6, xyz=[0, 9, -21], pbh=[-13.0, 0, 0], center_origin=True),

    # /images/2-wing-back-cabin.png
    CameraDefinition(name="Left wing flaps (cabin)", zoom=0.5, xyz=[-1.26, 0.6, -21.76], pbh=[-17, 0, -90], is_cabin=True),
    CameraDefinition(name="Right wing flaps (cabin)", zoom=0.5, xyz=[-1.26, 0.6, -21.76], pbh=[-17, 0, -90], is_cabin=True).get_mirrored(),

    # /images/3-wing-cabin.png
    CameraDefinition(name="Left wing (cabin)", zoom=0.5, xyz=[-1.25, 0.55, -18.01], pbh=[-12, 0, -90], is_cabin=True),
    CameraDefinition(name="Right wing (cabin)", zoom=0.5, xyz=[-1.25, 0.55, -18.01], pbh=[-12, 0, -90], is_cabin=True).get_mirrored(),

    # /images/4-wing-front-cabin.png
    CameraDefinition(name="Left engine (cabin)", zoom=0.5, xyz=[-1.25, 0.57, -12.49], pbh=[-24, 0, -90], is_cabin=True),
    CameraDefinition(name="Right engine (cabin)", zoom=0.5, xyz=[-1.25, 0.57, -12.49], pbh=[-24, 0, -90], is_cabin=True).get_mirrored(),

    # /images/5-wing-front.png
    CameraDefinition(name="Left engine", zoom=0.65, xyz=[-1.51, 0.68, -5.5], pbh=[-15, 0, -154]),
    CameraDefinition(name="Right engine", zoom=0.65, xyz=[-1.51, 0.68, -5.5], pbh=[-15, 0, -154]).get_mirrored(),

    # /images/6-wing-back.png
    CameraDefinition(name="Left wing", zoom=0.4, xyz=[-2.1, 1.4, -12.1], pbh=[0, 0, -40], center_origin=True),
    CameraDefinition(name="Right wing", zoom=0.4, xyz=[-2.1, 1.4, -12.1], pbh=[0, 0, -40], center_origin=True).get_mirrored(),

    # /images/7-wing.png
    CameraDefinition(name="Left wing 2", zoom=0.35, xyz=[-1.95, 1.7, -3.55], pbh=[-10, 0, -90], center_origin=True),
    CameraDefinition(name="Right wing 2", zoom=0.35, xyz=[-1.95, 1.7, -3.55], pbh=[-10, 0, -90], center_origin=True).get_mirrored(),

    # /images/8-wing-tip.png
    CameraDefinition(name="Left wing 3", zoom=0.65, xyz=[-16.45, 1.1, -21.8], pbh=[-27, 0, 63]),
    CameraDefinition(name="Right wing 3", zoom=0.65, xyz=[-16.45, 1.1, -21.8], pbh=[-27, 0, 63]).get_mirrored(),

    # /images/9-engine-side.png
    CameraDefinition(name="Left engine 2", zoom=0.65, xyz=[-12, 0.4, -2.5], pbh=[-5, 0, 65], center_origin=True),
    CameraDefinition(name="Right engine 2", zoom=0.65, xyz=[-12, 0.4, -2.5], pbh=[-5, 0, 65], center_origin=True).get_mirrored(),

     # /images/10-engine-front.png
    CameraDefinition(name="Left engine closeup", zoom=0.5, xyz=[-5.18, -2.1, -9.26], pbh=[0, 0, -180]),
    CameraDefinition(name="Right engine closeup", zoom=0.5, xyz=[-5.18, -2.1, -9.26], pbh=[0, 0, -180]).get_mirrored(),

    # /images/11-engine-back.png    
    CameraDefinition(name="Left gear", zoom=0.35, xyz=[-1, -1.65, -23.3], pbh=[-10, 0, -35]),
    CameraDefinition(name="Right gear", zoom=0.35, xyz=[-1, -1.65, -23.3], pbh=[-10, 0, -35]).get_mirrored(),

    # /images/12-side.png
    CameraDefinition(name="Left side", zoom=0.2, xyz=[-50, 2, -3], pbh=[-5, 0, 90], center_origin=True),
    CameraDefinition(name="Right side", zoom=0.2, xyz=[-50, 2, -3], pbh=[-5, 0, 90], center_origin=True).get_mirrored(),

    # /images/13-nose.png
    CameraDefinition(name="Nose", zoom=0.06, xyz=[0, -1.7, 80], pbh=[2, 0, 180], center_origin=True),

    # /images/14-gear.png
    CameraDefinition(name="Left gear 2", zoom=0.6, xyz=[-3.8, -1.9, -3.9], pbh=[0, 0, 0], center_origin=True),
    CameraDefinition(name="Right gear 2", zoom=0.6, xyz=[-3.8, -1.9, -3.9], pbh=[0, 0, 0], center_origin=True).get_mirrored(),

    # /images/15-belly.png
    CameraDefinition(name="Belly", zoom=1, xyz=[0, -1.5, -10], pbh=[0, 0, 0], center_origin=True),
]

CAM_DEF_TEMPLATE = """
[CAMERADEFINITION.{index}]
Title="{title}"
Guid="{{{guid}}}"
UITitle="{title}"
Description=""
Origin="Center"
Track="None"
TargetCategory="None"
ClipMode="Normal"
SnapPbhAdjust="None"
PanPbhAdjust="None"
XyzAdjust=0
ShowAxis="NO"
AllowZoom=1
InitialZoom={zoom}
SmoothZoomTime=5
BoundingBoxRadius=0.1
ShowWeather=0
CycleHidden=0
CycleHideRadius=0
ShowPanel=0
MomentumEffect=0
ShowLensFlare=0
PanPbhReturn=0
SnapPbhReturn=1
InstancedBased=0
NoSortTitle=0
Transition=0
Category="FixedOnPlane"
SubCategory="{sub_category}"
SubCategoryItem="None"
InitialXyz={xyz[0]}, {xyz[1]}, {xyz[2]}
InitialPbh={pbh[0]}, {pbh[1]}, {pbh[2]}
"""

if __name__ == "__main__":
    main()