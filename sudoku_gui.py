import os
import pygame
import sudoku
pygame.init()


class board(object):
    def __init__(self,asset_folder):
        
        #information from text board.
        self.initial_state = [["-"]*9 for i in range(9)]
        self.current_state = [["-"]*9 for i in range(9)]
        self.color_state = [[1]*9 for i in range(9)]
        self.S = "123456789-"

        #set attribute to value specific to image files.
        self.load_board_image(asset_folder)
        col = ["black","blue","red"]
        self.nums = dict([(i,self.load_num_images(asset_folder,i)) for i in col])
        
        #information for selected grid.
        self.sel_grid_coord = []
        

    def load_board_image(self,asset_folder):
        self.sudoku_board_image = pygame.image.load(os.path.join(asset_folder,"grid.jpg"))
        self.thick_line_width = 2
        self.thin_line_width  = 3
        self.small_grid_side = 36
        
    def load_num_images(self,asset_folder,color):
        def set_path(filename):
            return os.path.join(asset_folder,filename)
        return list(map(pygame.image.load,list(map(set_path,list(map(lambda i:i+"_"+color+".png",list(self.S)))))))

    def grid_to_xy(self,i,j):
        return (((j//3+1)*self.thick_line_width+(j+1)*self.thin_line_width+j*self.small_grid_side),
        ((i//3+1)*self.thick_line_width+(i+1)*self.thin_line_width+i*self.small_grid_side))

    def xy_to_grid(self,x,y):
        return ((y-self.thin_line_width-self.thick_line_width)//(self.small_grid_side+self.thin_line_width+self.thick_line_width//3),
        (x-self.thin_line_width-self.thick_line_width)//(self.small_grid_side+self.thin_line_width+self.thick_line_width//3))
        
    def set_from(self,display,state):
        self.initial_state = [[state[i][j] for j in range(9)] for i in range(9)]
        self.current_state = [[state[i][j] for j in range(9)] for i in range(9)]
        self.color_state = [[1]*9 for j in range(9)]

    def set_current_from(self,display,state):
        self.current_state = [[state[i][j] for j in range(9)] for i in range(9)]
        self.color_state = [[1]*9 for j in range(9)] 

    def render(self,display):
        display.blit(self.sudoku_board_image,(0,0))
        for i in range(9):
            for j in range(9):
                x,y = self.grid_to_xy(i,j)
                if self.initial_state[i][j]!="-":
                    col = "black"
                elif self.color_state[i][j]==3:
                    col = "red"
                else:
                    col = "blue"
                display.blit(self.nums[col][self.S.index(self.current_state[i][j])],
                                (x,y,self.small_grid_side-2,self.small_grid_side-2))

        if self.sel_grid_coord :
            i,j= self.sel_grid_coord
            x,y = self.grid_to_xy(i,j)
            if self.initial_state[i][j]=="-":
                col = (0,255,0)
            else:
                col = (255,0,0)
            pygame.draw.rect(display,col,(x-1,y-1,self.small_grid_side,self.small_grid_side),3)
        
    def index_select_grid(self,i,j):
        if i in range(9) and j in range(9):
            self.sel_grid_coord = [i,j]
            return True
        return False

    def mouse_select_grid(self,x,y):
        return self.index_select_grid(*self.xy_to_grid(x,y))
        
    
    def key_select_grid(self,up,down,right,left):
        if self.sel_grid_coord:
            i,j = self.sel_grid_coord
            if up==1 and down==0 and right==0 and left==0:
                i = (i-1)%9
            elif up==0 and down==1 and right==0 and left==0:
                i = (i+1)%9
            elif up==0 and down==0 and right==0 and left==1:
                j = (j-1)%9
            elif up==0 and down==0 and right==1 and left==0:
                j = (j+1)%9
            return self.index_select_grid(i,j)
        else:
            return self.index_select_grid(0,0)
    
    def change_sel_grid(self,v,col):
        if self.sel_grid_coord:
            i,j = self.sel_grid_coord
            if self.initial_state[i][j]=="-":
                self.current_state[i][j]=v
                self.color_state[i][j]=col
            


class button:
    def __init__(self,x,y,width,height,action,active=True,color = (0,0,0),text = "",font= pygame.font.get_default_font(),font_size = 10,font_color = (255,255,255),img = None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.action = action
        self.active = active
        self.color = color
        self.text = text
        self.font = font
        self.font_size = font_size
        self.font_color = font_color
        self.image = img
    def render(self,display):
        if self.active:
            pygame.draw.rect(display,self.color,(self.x,self.y,self.width,self.height))
            f_text = pygame.font.Font(self.font,self.font_size)
            TextSurf = f_text.render(self.text,True,self.font_color)
            TextRect = TextSurf.get_rect()
            TextRect.center = ((self.x+ self.width//2),(self.y+self.height//2))
            display.blit(TextSurf,TextRect)
    def get_pressed(self,click,mouse_pos):
        if self.active and  click[0]==1:
            if (mouse_pos[0]>=self.x and mouse_pos[0]<=self.x+self.width and
                mouse_pos[1]>=self.y and mouse_pos[1]<=self.y+self.height):
                self.action()
                return True
        return False
                    
            
Mats = []
M = """5 3 - - 7 - - - -
6 - - 1 9 5 - - -
- 9 8 - - - - 6 -
8 - - - 6 - - - 3
4 - - 8 - 3 - - 1
7 - - - 2 - - - 6
- 6 - - - - 2 8 -
- - - 4 1 9 - - 5
- - - - 8 - - 7 9"""
M = M.split()
M = [ M[9*i:9*i+9] for i in range(9)]
Mats.append(M)
M = ["2 4 - - - - 1 - 7",
         "6 - 8 9 1 5 3 - 2",
         "9 - - - 2 7 - 6 -",
         "- 9 7 1 3 2 6 - 5",
         "- - - 5 - 8 - 3 4",
         "5 - - - - - - - -",
         "7 - 2 3 - 9 8 - 1",
         "- - - 8 - - - - -",
         "- 1 9 - - - 4 7 -"]
M = [M[i].split() for i in range(9)]
Mats.append(M)
display_width = 359
display_height = 400
display = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Sudoku')

i_m = 0

clock = pygame.time.Clock()
run = True
B = board("assets")
s = sudoku.solver()
s2 = sudoku.solver()
solve = False
reset = False
editable = True
see_solution = False

B.set_from(display,Mats[i_m])

def a_reset():
    global reset,editable,solve,B,s,ss
    B.set_from(display,B.initial_state)
    s.set_from(B.initial_state)
    ss = s.solve(is_pausable=True)
    editable = True
    solve = False
    reset = False

def a_solve():
    global editable,solve,B,ss
    editable = False
    q = next(ss)
    if not(q==1 or q==-1):
        B.index_select_grid(q[0],q[1])
        B.change_sel_grid(q[2],2)
        solve = True
    else:
        solve = False

def a_show_solution():
    global see_solution,editable,solve,B,s2,ss
    editable = False
    B.set_current_from(display,s2.M)
    solve = False
    see_solution = False

def a_new_game():
    global reset,editable,solve,see_solution,B,s,ss,s2,ss2,i_m,Mats
    i_m = (i_m+1)%len(Mats)
    solve = False
    reset = False
    editable = True
    see_solution = False
    B.set_from(display,Mats[i_m])
    s.set_from(Mats[i_m])
    ss = s.solve(is_pausable=True)
    s2.set_from(Mats[i_m])
    ss2 = s2.solve(is_pausable=False)

a_new_game()
    
b1 = button(20,365,50,30,a_reset,text = "Reset",font_size = 15)
b2 = button(300,365,50,30,a_solve,text = "Solve",font_size = 15)
b3 = button(300,365,50,30,a_show_solution,active = False,text = "Finish",font_size = 15)
b4 = button(130,365,100,30,a_new_game,text = "New game",font_size = 15)

display.fill((100,100,100))

num_keys = [pygame.K_1,pygame.K_2,pygame.K_3,pygame.K_4,pygame.K_5,
            pygame.K_6,pygame.K_7,pygame.K_8,pygame.K_9,pygame.K_BACKSPACE]
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        click = pygame.mouse.get_pressed()
        mouse = pygame.mouse.get_pos()
        key_press = pygame.key.get_pressed()
        i = -1
        for k in range(len(num_keys)):
            if key_press[num_keys[k]]==1:
                i = k
                break
        if key_press[pygame.K_SPACE]==1:
            solve = True
        if key_press[pygame.K_RETURN]==1:
            see_solution = True
        if key_press[pygame.K_r]==1:
            a_reset()
        b1.get_pressed(click,mouse)
        b2.get_pressed(click,mouse)
        b3.get_pressed(click,mouse)
        b4.get_pressed(click,mouse)
        if not (solve or reset) and editable:
            if click[0]==1:
                B.mouse_select_grid(mouse[0],mouse[1])
            if i==-1:
                B.key_select_grid(key_press[pygame.K_UP],key_press[pygame.K_DOWN],
                                  key_press[pygame.K_RIGHT],key_press[pygame.K_LEFT])
            else:
                s.set_from(B.current_state)
                tm = s.is_valid_move(B.sel_grid_coord[0],B.sel_grid_coord[1],i)
                if tm:
                    B.change_sel_grid(B.S[i],2)
                else:
                    B.change_sel_grid(B.S[i],3)
    if solve and (not reset):
        a_solve()
        b2.active = False
        b3.active = True
    elif not solve:
        b2.active = True
        b3.active = False
    B.render(display)
    b1.render(display)
    b2.render(display)
    b3.render(display)
    b4.render(display)
    pygame.display.update()
    clock.tick(60)

pygame.quit()

    
    
