"""Real-ESRGAN x4plus en CPU (arquitectura RRDBNet), sin basicsr."""
import sys, os, torch, numpy as np
from torch import nn
import torch.nn.functional as F
from PIL import Image

class RDB(nn.Module):
    def __init__(s, nf=64, gc=32):
        super().__init__()
        s.conv1 = nn.Conv2d(nf, gc, 3, 1, 1); s.conv2 = nn.Conv2d(nf + gc, gc, 3, 1, 1)
        s.conv3 = nn.Conv2d(nf + 2 * gc, gc, 3, 1, 1); s.conv4 = nn.Conv2d(nf + 3 * gc, gc, 3, 1, 1)
        s.conv5 = nn.Conv2d(nf + 4 * gc, nf, 3, 1, 1); s.lrelu = nn.LeakyReLU(0.2, True)
    def forward(s, x):
        x1 = s.lrelu(s.conv1(x)); x2 = s.lrelu(s.conv2(torch.cat((x, x1), 1)))
        x3 = s.lrelu(s.conv3(torch.cat((x, x1, x2), 1))); x4 = s.lrelu(s.conv4(torch.cat((x, x1, x2, x3), 1)))
        return s.conv5(torch.cat((x, x1, x2, x3, x4), 1)) * 0.2 + x

class RRDB(nn.Module):
    def __init__(s, nf=64, gc=32):
        super().__init__(); s.rdb1 = RDB(nf, gc); s.rdb2 = RDB(nf, gc); s.rdb3 = RDB(nf, gc)
    def forward(s, x):
        return s.rdb3(s.rdb2(s.rdb1(x))) * 0.2 + x

class RRDBNet(nn.Module):
    def __init__(s, nb=23, nf=64, gc=32):
        super().__init__()
        s.conv_first = nn.Conv2d(3, nf, 3, 1, 1)
        s.body = nn.Sequential(*[RRDB(nf, gc) for _ in range(nb)])
        s.conv_body = nn.Conv2d(nf, nf, 3, 1, 1)
        s.conv_up1 = nn.Conv2d(nf, nf, 3, 1, 1); s.conv_up2 = nn.Conv2d(nf, nf, 3, 1, 1)
        s.conv_hr = nn.Conv2d(nf, nf, 3, 1, 1); s.conv_last = nn.Conv2d(nf, 3, 3, 1, 1)
        s.lrelu = nn.LeakyReLU(0.2, True)
    def forward(s, x):
        f = s.conv_first(x); f = f + s.conv_body(s.body(f))
        f = s.lrelu(s.conv_up1(F.interpolate(f, scale_factor=2, mode='nearest')))
        f = s.lrelu(s.conv_up2(F.interpolate(f, scale_factor=2, mode='nearest')))
        return s.conv_last(s.lrelu(s.conv_hr(f)))

def main():
    weights, outdir, files = sys.argv[1], sys.argv[2], sys.argv[3:]
    net = RRDBNet()
    sd = torch.load(weights, map_location='cpu')
    net.load_state_dict(sd.get('params_ema', sd.get('params', sd)), strict=True)
    net.eval(); torch.set_num_threads(os.cpu_count() or 2)
    tile, pad = 192, 12
    for fp in files:
        img = np.asarray(Image.open(fp).convert('RGB')).astype(np.float32) / 255.
        h, w, _ = img.shape
        x = torch.from_numpy(img).permute(2, 0, 1)[None]
        out = torch.zeros(1, 3, h * 4, w * 4)
        with torch.no_grad():
            for y0 in range(0, h, tile):
                for x0 in range(0, w, tile):
                    y1, x1 = min(y0 + tile, h), min(x0 + tile, w)
                    ya, xa = max(y0 - pad, 0), max(x0 - pad, 0)
                    yb, xb = min(y1 + pad, h), min(x1 + pad, w)
                    o = net(x[:, :, ya:yb, xa:xb]).clamp(0, 1)
                    out[:, :, y0*4:y1*4, x0*4:x1*4] = o[:, :, (y0-ya)*4:(y0-ya)*4+(y1-y0)*4, (x0-xa)*4:(x0-xa)*4+(x1-x0)*4]
        res = (out[0].permute(1, 2, 0).numpy() * 255).round().astype(np.uint8)
        name = os.path.splitext(os.path.basename(fp))[0]
        Image.fromarray(res).save(os.path.join(outdir, name + '.png'))
        print('ok', name, w, h, flush=True)

if __name__ == '__main__':
    main()
