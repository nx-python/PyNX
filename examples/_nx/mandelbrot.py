import _nx

GfxMode_LinearDouble = 2
WIDTH = 1280
HEIGHT = 720
MAX_ITER = 32

palette_r = [0, 8, 16, 24, 32, 40, 42, 38, 32, 22, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 22, 57, 96, 137, 182, 216, 224, 232, 240, 248]
palette_g = [0, 1, 6, 13, 24, 37, 48, 56, 64, 72, 80, 88, 96, 104, 112, 120, 128, 110, 90, 66, 40, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
palette_b = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 24, 45, 70, 97, 128, 136, 144, 152, 160, 168, 176, 184, 192, 200, 208, 202, 168, 130, 90, 46]

def mandel(x0, y0):
    x, y = (0.0, 0.0)
    for i in range(MAX_ITER):
        x, y = ( (x*x - y*y + x0), (2*x*y + y0) )
        if (x*x + y*y) >= 4:
            return i
    return 0

_nx.gfx_set_mode(GfxMode_LinearDouble)

fb = bytearray([0]*WIDTH*HEIGHT*4)  # RGBA8888

for y in range(HEIGHT):
    y0 = (y/HEIGHT*2)-1
    for x in range(WIDTH):
        x0 = (x/HEIGHT*2)-2.5
        iterations = mandel(x0, y0)
        fb[(y*WIDTH+x)*4] = palette_r[iterations]
        fb[(y*WIDTH+x)*4+1] = palette_g[iterations]
        fb[(y*WIDTH+x)*4+2] = palette_b[iterations]

    _nx.gfx_set_framebuffer(fb)
    _nx.gfx_flush_and_sync()
