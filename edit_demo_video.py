import os
import time
import numpy as np
from PIL import Image
import moviepy as mp
from moviepy import vfx

SOURCE_VIDEO = r"C:\Users\akash\Videos\Screen Recordings\Screen Recording 2026-10-17 194926.mp4"
INTRO_CARD = r"c:\Users\akash\Downloads\agentshield\agentshield\.video_preview\intro_card.png"
OUTRO_CARD = r"c:\Users\akash\Downloads\agentshield\agentshield\.video_preview\outro_card.png"
FF_BADGE = r"c:\Users\akash\Downloads\agentshield\agentshield\.video_preview\ff_badge.png"

OUTPUT_WORKSPACE = r"c:\Users\akash\Downloads\agentshield\agentshield\HYDRA_Demo_Final.mp4"
OUTPUT_USER_FOLDER = r"C:\Users\akash\Videos\Screen Recordings\HYDRA_Demo_Final.mp4"

def main():
    print("[1/5] Loading source video and graphic assets...")
    source = mp.VideoFileClip(SOURCE_VIDEO)
    w, h = source.size
    print(f"      Source resolution: {w}x{h}, duration: {source.duration:.2f}s, fps: {source.fps}")

    # 1. Intro Card (3.5s)
    intro_clip = mp.ImageClip(INTRO_CARD).with_duration(3.5).with_fps(30)

    # 2. Segment A: Initial overview + opening sidebar (0.0s to 7.5s)
    seg_a = source.subclipped(0.0, 7.5)

    # 3. Segment B: Repo connected & vector review (59.0s to 81.5s)
    seg_b = source.subclipped(59.0, 81.5)

    # 4. Segment C: Execution spinner sped up 8x with badge overlay (81.5s to 145.5s)
    seg_c_raw = source.subclipped(81.5, 145.5)
    seg_c_fast = seg_c_raw.with_effects([vfx.MultiplySpeed(8.0)])

    # Load badge
    badge_img = Image.open(FF_BADGE).convert("RGBA")
    badge_arr = np.array(badge_img)
    bw, bh = badge_img.size
    bx0 = (w - bw) // 2
    by0 = h - bh - 35
    alpha = badge_arr[:, :, 3:] / 255.0
    badge_rgb = badge_arr[:, :, :3]

    def overlay_badge(frame):
        f = frame.copy()
        f[by0:by0+bh, bx0:bx0+bw] = (
            alpha * badge_rgb + (1 - alpha) * f[by0:by0+bh, bx0:bx0+bw]
        ).astype(np.uint8)
        return f

    seg_c = seg_c_fast.image_transform(overlay_badge)

    # 5. Segment D: Results, trace inspection & commit remediation (145.5s to 189.0s)
    seg_d = source.subclipped(145.5, 189.0)

    # 6. Outro Card (4.0s)
    outro_clip = mp.ImageClip(OUTRO_CARD).with_duration(4.0).with_fps(30)

    print("[2/5] Concatenating clips into master sequence...")
    clips = [intro_clip, seg_a, seg_b, seg_c, seg_d, outro_clip]
    final = mp.concatenate_videoclips(clips, method="compose")

    print(f"      Total timeline duration: {final.duration:.2f} seconds (~{int(final.duration)//60}m {int(final.duration)%60:02d}s)")

    print(f"[3/5] Rendering final video to: {OUTPUT_WORKSPACE}...")
    t0 = time.time()
    final.write_videofile(
        OUTPUT_WORKSPACE,
        fps=30,
        codec="libx264",
        preset="fast",
        audio=False,
        ffmpeg_params=["-pix_fmt", "yuv420p", "-crf", "20"]
    )
    print(f"      Render completed in {time.time() - t0:.1f}s")

    # Copy to user's screen recordings folder
    print(f"[4/5] Copying finalized video to user directory: {OUTPUT_USER_FOLDER}...")
    import shutil
    shutil.copy2(OUTPUT_WORKSPACE, OUTPUT_USER_FOLDER)

    # Clean up
    source.close()
    final.close()
    print("[5/5] Video generation fully finished!")

if __name__ == "__main__":
    main()
