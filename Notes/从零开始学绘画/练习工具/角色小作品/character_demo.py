"""Drawing course 39–42: local PNG expression player; no third-party packages.

Run: python character_demo.py
Check scheduling without opening a window: python character_demo.py --self-test
"""
from pathlib import Path
import math
import sys
import time

FILES = {"open": "open.png", "half": "half.png", "closed": "closed.png", "smile": "smile.png"}
NAMES = {"open": "睁眼", "half": "半闭", "closed": "闭眼", "smile": "微笑"}
SEQUENCE = ("open", "half", "closed", "half", "open")
TIMINGS = {
    "短眨练习（3 秒）": (1000, 80, 80, 80, 1760),
    "等时对照（3 秒）": (600, 600, 600, 600, 600),
    "慢放检查（12 秒）": (4000, 320, 320, 320, 7040),
}
SMILE_MS = 900


def check_durations(durations):
    values = tuple(durations)
    if len(values) != 5 or any(type(x) is not int or x <= 0 for x in values):
        raise ValueError("五段停留时间必须是正整数毫秒。")
    return values


def frame_at(elapsed_ms, durations):
    """Choose a state from elapsed time, rather than counting timer callbacks."""
    phase = max(0, elapsed_ms) % sum(durations)
    for state, duration in zip(SEQUENCE, durations):
        if phase < duration:
            return state
        phase -= duration
    return "open"


class Player:
    """One owner of the current expression; the GUI only displays its result."""

    def __init__(self, now_ms=0):
        self.durations = TIMINGS["短眨练习（3 秒）"]
        self.epoch = now_ms
        self.smile_until = None
        self.paused = True
        self.manual = "open"

    def current(self, now_ms):
        if self.paused:
            return self.manual
        if self.smile_until is not None:
            if now_ms < self.smile_until:
                return "smile"
            # A response ends with a fresh open hold, never an old half-blink.
            self.smile_until = None
            self.epoch = now_ms
        return frame_at(now_ms - self.epoch, self.durations)

    def smile(self, now_ms):
        self.paused = False
        self.smile_until = now_ms + SMILE_MS

    def select(self, state):
        if state not in FILES:
            raise ValueError("未知的表情状态。")
        self.paused = True
        self.manual = state
        self.smile_until = None

    def play(self, now_ms):
        self.epoch = now_ms
        self.smile_until = None
        self.paused = False

    def pause(self, now_ms):
        state = self.current(now_ms)
        self.select(state)

    def set_timing(self, durations, now_ms):
        values = check_durations(durations)
        was_paused = self.paused
        self.durations = values
        self.play(now_ms)
        if was_paused:
            self.select("open")


def validate_dimensions(sizes):
    if set(sizes) != set(FILES):
        raise ValueError("需要 open、half、closed、smile 四种状态。")
    values = list(sizes.values())
    if any(len(x) != 2 or min(x) <= 0 for x in values):
        raise ValueError("图片尺寸无效。")
    if len(set(values)) != 1:
        detail = "；".join(f"{FILES[k]}: {w}×{h}" for k, (w, h) in sizes.items())
        raise ValueError("四张图片尺寸必须相同。" + detail)
    return values[0]


def load_frames(tk_module, master, folder):
    """Load into a temporary dictionary; bad input never replaces the old set."""
    folder = Path(folder)
    missing = [name for name in FILES.values() if not (folder / name).is_file()]
    if missing:
        raise ValueError("缺少：" + "、".join(missing))
    frames = {
        state: tk_module.PhotoImage(master=master, file=str(folder / name), format="png")
        for state, name in FILES.items()
    }
    width, height = validate_dimensions({key: (im.width(), im.height()) for key, im in frames.items()})
    # Every frame shares one factor and one canvas anchor. Original files stay intact.
    factor = max(1, math.ceil(max(width, height) / 480))
    display = {key: im.subsample(factor, factor) for key, im in frames.items()}
    return frames, display, (width, height), factor


def launch():
    import tkinter as tk
    from tkinter import ttk, filedialog, messagebox

    class DrawingApp:
        def __init__(self, root):
            self.root = root
            self.player = Player(self.now())
            self.raw = None
            self.frames = None
            self.timer = None
            self.last_render = None
            self.closing = False
            root.title("我的角色小作品 · 绘画课 39—42")
            root.resizable(False, False)
            outer = ttk.Frame(root, padding=14)
            outer.pack()
            ttk.Label(outer, text="我的角色小作品", font=("Microsoft YaHei", 17)).pack(anchor="w")
            self.source = tk.StringVar(value="示意模式：程序绘制的简化脸。选择自己的四张 PNG 后替换。")
            ttk.Label(outer, textvariable=self.source, wraplength=530).pack(anchor="w", pady=(6, 10))
            self.canvas = tk.Canvas(outer, width=480, height=480, bg="#edf2f8", highlightthickness=0)
            self.canvas.pack()
            self.canvas.bind("<Button-1>", self.respond)
            self.status = tk.StringVar()
            ttk.Label(outer, textvariable=self.status).pack(anchor="w", pady=7)
            row = ttk.Frame(outer)
            row.pack(fill="x", pady=3)
            self.play_button = ttk.Button(row, text="播放", command=self.toggle)
            self.play_button.pack(side="left")
            for state in FILES:
                ttk.Button(row, text=NAMES[state], width=6, command=lambda s=state: self.manual(s)).pack(side="left", padx=3)
            self.guides = tk.BooleanVar(value=False)
            ttk.Checkbutton(row, text="十字参考线", variable=self.guides, command=self.paint).pack(side="left", padx=5)
            options = ttk.Frame(outer)
            options.pack(fill="x", pady=6)
            ttk.Label(options, text="节奏：").pack(side="left")
            self.timing = tk.StringVar(value="短眨练习（3 秒）")
            combo = ttk.Combobox(options, state="readonly", values=list(TIMINGS), textvariable=self.timing, width=23)
            combo.pack(side="left")
            combo.bind("<<ComboboxSelected>>", self.change_timing)
            ttk.Button(options, text="点击微笑", command=self.respond).pack(side="left", padx=8)
            files_row = ttk.Frame(outer)
            files_row.pack(fill="x", pady=5)
            ttk.Button(files_row, text="载入我的图片文件夹", command=self.choose).pack(side="left")
            ttk.Button(files_row, text="恢复示意", command=self.reset).pack(side="left", padx=8)
            ttk.Label(outer, text="点击画面：微笑约 0.9 秒后回到睁眼，再恢复眨眼。\n手动状态按钮会暂停；图片只在本机读取，不修改原文件。", wraplength=530).pack(anchor="w", pady=(5, 0))
            root.protocol("WM_DELETE_WINDOW", self.close)
            initial = Path(__file__).resolve().parent / "my_frames"
            if all((initial / name).is_file() for name in FILES.values()):
                self.use_folder(initial)
            self.tick()

        @staticmethod
        def now():
            return time.monotonic() * 1000

        def manual(self, state):
            self.player.select(state)
            self.paint()

        def toggle(self):
            now = self.now()
            if self.player.paused:
                self.player.play(now)
            else:
                self.player.pause(now)
            self.paint()

        def respond(self, event=None):
            self.player.smile(self.now())
            self.paint()

        def change_timing(self, event=None):
            self.player.set_timing(TIMINGS[self.timing.get()], self.now())
            self.paint()

        def choose(self):
            self.player.pause(self.now())
            folder = filedialog.askdirectory(parent=self.root, title="选择含四张 PNG 的文件夹")
            if folder:
                self.use_folder(folder)
            self.paint()

        def use_folder(self, folder):
            try:
                raw, display, size, factor = load_frames(tk, self.root, folder)
            except (ValueError, OSError, tk.TclError) as exc:
                messagebox.showerror("没有载入图片", str(exc), parent=self.root)
                return
            self.raw, self.frames = raw, display
            self.source.set(f"已载入自己的图片：{size[0]} × {size[1]}；显示为原图的 1/{factor}。\n{folder}")
            self.last_render = None
            self.player.select("open")

        def reset(self):
            self.frames = None
            self.raw = None
            self.last_render = None
            self.player.select("open")
            self.source.set("示意模式：程序绘制的简化脸。选择自己的四张 PNG 后替换。")
            self.paint()

        def paint(self):
            state = self.player.current(self.now())
            self.play_button.configure(text="播放" if self.player.paused else "暂停")
            mode = "已暂停" if self.player.paused else "微笑反馈" if self.player.smile_until else "正在眨眼"
            self.status.set(f"当前：{NAMES[state]} · {mode}")
            key = (state, self.guides.get(), id(self.frames))
            if key == self.last_render:
                return
            self.last_render = key
            c = self.canvas
            c.delete("all")
            if self.frames:
                c.create_image(240, 240, image=self.frames[state], anchor="center")
            else:
                # Code-native diagram only; not a substitute for the learner's artwork.
                c.create_oval(98, 50, 382, 420, fill="#ffe4d5", outline="#476487", width=3)
                c.create_line(120, 110, 180, 65, 240, 110, 300, 65, 360, 110, fill="#749bce", width=22, smooth=True)
                for x in (167, 313):
                    c.create_line(x-34, 173, x, 168, x+34, 173, fill="#667994", width=3, smooth=True)
                    if state == "closed":
                        c.create_line(x-36, 245, x, 259, x+36, 245, fill="#344966", width=3, smooth=True)
                    else:
                        c.create_oval(x-38, 208, x+38, 275, fill="white", outline="#344966", width=3)
                        c.create_oval(x-22, 212, x+22, 271, fill="#729ed7", outline="")
                        c.create_oval(x-9, 228, x+9, 254, fill="#344966", outline="")
                        c.create_oval(x-13, 218, x-4, 227, fill="white", outline="")
                        if state == "half":
                            c.create_rectangle(x-41, 201, x+41, 243, fill="#ffe4d5", outline="")
                            c.create_line(x-37, 243, x+37, 243, fill="#344966", width=3)
                c.create_line(237, 297, 241, 301, fill="#bc998a", width=2)
                if state == "smile":
                    c.create_line(215, 328, 240, 340, 265, 328, smooth=True, fill="#89615c", width=3)
                else:
                    c.create_line(226, 331, 254, 331, fill="#89615c", width=2)
            if self.guides.get():
                c.create_line(240, 0, 240, 480, fill="#3487d6", dash=(5, 4))
                c.create_line(0, 240, 480, 240, fill="#3487d6", dash=(5, 4))

        def tick(self):
            if not self.closing:
                self.paint()
                self.timer = self.root.after(25, self.tick)

        def close(self):
            self.closing = True
            if self.timer is not None:
                self.root.after_cancel(self.timer)
            self.root.destroy()

    root = tk.Tk()
    DrawingApp(root)
    root.mainloop()


def self_test():
    timing = TIMINGS["短眨练习（3 秒）"]
    # Boundary checks follow the editable durations, so changing the closed
    # hold in lesson 40 does not make an otherwise valid preset fail.
    elapsed = 0
    for expected, duration in zip(("open", "half", "closed", "half", "open"), timing):
        assert frame_at(elapsed, timing) == expected
        assert frame_at(elapsed + duration - 1, timing) == expected
        elapsed += duration
    assert frame_at(elapsed, timing) == "open"
    assert frame_at(elapsed + timing[0], timing) == "half"
    p = Player()
    assert p.current(1000) == "open"  # Initially paused.
    p.play(0)
    assert p.current(1080) == "closed"
    p.smile(1100)
    assert p.current(1150) == "smile"  # Blink cannot overwrite the smile.
    p.smile(1700)
    assert p.current(2200) == "smile"  # Repeated click extends one deadline.
    assert p.current(2600) == "open"
    assert p.current(3600) == "half"
    p.pause(3610)
    assert p.current(99999) == "half"
    p.select("closed")
    assert p.current(200000) == "closed"
    p.set_timing(TIMINGS["等时对照（3 秒）"], 200000)
    assert p.paused and p.current(200000) == "open"
    p.play(0)
    assert p.current(600) == "half"
    assert p.current(1200) == "closed"
    assert validate_dimensions({key: (480, 480) for key in FILES}) == (480, 480)
    for sizes in [{"open": (480, 480)}, {key: (240 if key == "half" else 480, 480) for key in FILES}]:
        try:
            validate_dimensions(sizes)
        except ValueError:
            pass
        else:
            raise AssertionError("Bad dimensions accepted")
    for values in [(0, 80, 80, 80, 1000), (10,), (10, 20, True, 40, 50)]:
        try:
            check_durations(values)
        except ValueError:
            pass
        else:
            raise AssertionError("Bad durations accepted")
    print("PASS: timing boundaries, looping, click priority, repeated clicks, pause/resume, presets, dimension validation.")


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        self_test()
    else:
        try:
            launch()
        except ImportError:
            raise SystemExit("当前 Python 缺少 tkinter。请安装带 Tcl/Tk 的 Python；运行 python -m tkinter 检查。")
