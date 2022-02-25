import os
import shutil
from argparse import ArgumentParser
from pathlib import Path
from utils import ffmpeg


def main(args):
    input_path = Path(args.input)
    mask_path = Path(args.mask)
    output_video_path = input_path.parent / \
        f"{input_path.stem}_FGVC_result.mp4"

    video_frames_path = Path("/tmp/video_frames")
    mask_frames_path = Path("/tmp/mask_frames")
    output_path = Path("/tmp/result_frames")

    def cleanup():
        shutil.rmtree(video_frames_path, ignore_errors=True)
        shutil.rmtree(mask_frames_path, ignore_errors=True)
        shutil.rmtree(output_path, ignore_errors=True)

    cleanup()

    video_frames_path.mkdir(parents=True, exist_ok=True)
    mask_frames_path.mkdir(parents=True, exist_ok=True)
    output_path.mkdir(parents=True, exist_ok=True)

    output_video_fps: str
    # extract input frames, if necessary
    if input_path.is_file():
        output_video_fps = ffmpeg.get_fps(input_path)
        ffmpeg.extract_frames(input_path, video_frames_path)
    else:
        output_video_fps = "30"
        video_frames_path = input_path

    # extract mask frames, if necessary
    if mask_path.is_file():
       ffmpeg.extract_frames(mask_path, mask_frames_path)
    else:
       mask_frames_path = mask_path

    # run FGVC
    os.system(f'\
        cd tool && \
        python video_completion.py \
            --mode {"video_extrapolation" if args.extrapolate else "object_removal"} \
            --path \"{video_frames_path}\" \
            --path_mask \"{mask_frames_path}\" \
            --outroot \"{output_path}\" \
            {"--seamless" if args.seamless else ""} \
    ')

    # recombine output frames
    result_frames_path: str
    
    if args.seamless is True:
        result_frames_path = output_path / 'frame_seamless_comp_final'
    else:
        result_frames_path = output_path / 'frame_comp_final'
     
    ffmpeg.combine_frames(result_frames_path, output_video_path, fps=output_video_fps)

    cleanup()

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-i', '--input', type=str,
                        required=True, help='Input RGB video path')
    parser.add_argument('-m', '--mask', type=str, help='Input mask video path')
    parser.add_argument('-o', '--output', type=str, help='Output path')
    parser.add_argument('--extrapolate', action='store_true')
    parser.add_argument('--seamless', action='store_true')

    args = parser.parse_args()

    main(args)
