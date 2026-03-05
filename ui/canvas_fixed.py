# -*- coding: utf-8 -*-
"""
플롯 창에서 레이아웃 변경(탭 전환 등) 시 그래프가 아래로 밀리는 현상을 막기 위해,
리사이즈 후에도 figure 크기를 항상 6.5x6.5로 유지하는 FigureCanvas 서브클래스.
(고정 크기 캔버스와 함께 사용.)
"""

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg

FIGURE_SIZE_INCH = 6.5


class FixedFigureCanvas(FigureCanvasQTAgg):
    """리사이즈 후 figure를 6.5x6.5로 고정하여 그래프 위치가 밀리지 않도록 함."""

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.figure is None:
            return
        self.figure.set_size_inches(FIGURE_SIZE_INCH, FIGURE_SIZE_INCH, forward=False)
        self.draw_idle()
