from easygraphics import *

def main():
    init_graph(1000,1000)
    set_render_mode(RenderMode.RENDER_MANUAL)

    set_fill_color("white")
    #have different modes and enter a new function for each mode 
    typestr = "nothing"
    while is_run():
        x, y = get_cursor_pos()
        clear_device()
        # fill_rect(0, 580, 390, 600)
        draw_text(0, 600, "%d,%d" % (x, y))
        fill_rect(400, 580, 800, 600)
        draw_text(400, 600, "button %s at %d,%d" % (typestr, x, y))
        if typestr == "pressed":
            draw_rect(a,b,x,y)
            if b > y and x > a:
                set_font_size((b-y))
                draw_text(a,b,"hello")
            if b < y and x > a:
                set_font_size((y-b))
                draw_text(a,y,"hello")
            if b < y and x < a:
                set_font_size(y-b)
                draw_text(x,y,"hello")
            if b > y and x < a:
                set_font_size(b-y)
                draw_text(x,b,"hello")
            print(a,b,x,y)


        if has_mouse_msg():
            msg = get_mouse_msg()
            if msg.type == MouseMessageType.PRESS_MESSAGE:
                typestr = "pressed"
                a, b = get_cursor_pos()
            elif msg.type == MouseMessageType.RELEASE_MESSAGE:

                typestr = "released"
        delay_fps(200)

    close_graph()

easy_run(main)