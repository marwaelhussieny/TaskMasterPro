
import tkinter as tk
from config.settings import Config

class ModernButton(tk.Canvas):
    """Custom modern button widget"""
    
    def __init__(self, parent, text, command, bg_color=Config.SECONDARY_COLOR, 
                 fg_color=Config.TEXT_COLOR, width=200, height=40):
        super().__init__(parent, width=width, height=height, bg=Config.BG_COLOR, 
                        highlightthickness=0)
        
        self.command = command
        self.bg_color = bg_color
        self.hover_color = self._adjust_color(bg_color, 1.2)
        
        # Draw button
        self.button_id = self.create_rectangle(0, 0, width, height, 
                                               fill=bg_color, outline="")
        self.text_id = self.create_text(width//2, height//2, text=text, 
                                       fill=fg_color, font=Config.FONT_NORMAL)
        
        # Bind events
        self.bind("<Button-1>", lambda e: command())
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
    
    def _adjust_color(self, color, factor):
        """Lighten or darken color"""
        color = color.lstrip('#')
        r, g, b = int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16)
        r = min(255, int(r * factor))
        g = min(255, int(g * factor))
        b = min(255, int(b * factor))
        return f'#{r:02x}{g:02x}{b:02x}'
    
    def _on_enter(self, e):
        self.itemconfig(self.button_id, fill=self.hover_color)
    
    def _on_leave(self, e):
        self.itemconfig(self.button_id, fill=self.bg_color)


class ModernEntry(tk.Entry):
    """Styled entry widget"""
    
    def __init__(self, parent, placeholder="", **kwargs):
        super().__init__(parent, font=Config.FONT_NORMAL,
                        bg=Config.BG_COLOR, fg=Config.TEXT_COLOR,
                        insertbackground=Config.TEXT_COLOR, **kwargs)
        self.placeholder = placeholder
        self.placeholder_active = False
        
        if placeholder:
            self._show_placeholder()
            self.bind("<FocusIn>", self._clear_placeholder)
            self.bind("<FocusOut>", self._restore_placeholder)
    
    def _show_placeholder(self):
        if not self.get():
            self.insert(0, self.placeholder)
            self.config(fg=Config.TEXT_SECONDARY)
            self.placeholder_active = True
    
    def _clear_placeholder(self, e):
        if self.placeholder_active:
            self.delete(0, tk.END)
            self.config(fg=Config.TEXT_COLOR)
            self.placeholder_active = False
    
    def _restore_placeholder(self, e):
        if not self.get():
            self._show_placeholder()

