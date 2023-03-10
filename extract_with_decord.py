from torchdata.datapipes.iter import IterableWrapper
import argparse
from torch.utils.data import functional_datapipe
from torchdata.datapipes.iter import IterDataPipe
from decord import VideoReader
from PIL import Image

args = argparse.ArgumentParser()
args.add_argument("stride", type=int)
args = args.parse_args()


@functional_datapipe("load_frames_decord")
class DecordFrameLoader(IterDataPipe):

    def __init__(self,
                 src_pipeline,
                 stride=1,
                 from_key=None,
                 width=224,
                 height=224,
                 to_array=False,
                 to_images=False) -> None:
        # decord_args: width=224, height=224
        self.src_pipeline = src_pipeline
        self.from_key = from_key
        self.width = width
        self.height = height
        self.stride = stride
        self.to_images = to_images
        self.to_array = to_array

    def __iter__(self):
        for x in self.src_pipeline:
            # video_path_raw = x[self.from_key]
            # with open(video_path_raw, "rb") as f:
            buffer = x[self.from_key]
            vr = VideoReader(buffer, width=self.width, height=self.height)

            indices = list(range(0, len(vr), self.stride))
            arr = vr.get_batch(indices).asnumpy()

            if self.to_array:
                x[self.from_key + ".frame_arr"] = arr
            if self.to_images:
                x[self.from_key + ".frame_img"] = [Image.fromarray(_) for _ in arr]
            yield x


video = IterableWrapper([{"video": "./ZZXQF.mp4"}])
frames = iter(DecordFrameLoader(video, stride=args.stride, from_key="video", to_images=True)).__next__()["video.frame_img"]
print(f"Decord Extract #Frames {len(frames)}")