import os
import pygame
import sudoku
pygame.init()


class board(object):
    def __init__(self,asset_folder):
        def set_path(filename):
            return os.path.join(asset_folder,filename)
        #set attribute to value specific to image files.
        self.sudoku_board_image = pygame.image.load(set_path("grid.jpg"))
        self.thick_line_width = 2
        self.thin_line_width  = 3
        self.small_grid_side = 36
        self.nums_blk = list(map(pygame.image.load,
                        list(map(set_path,
        ["1_black.png","2_black.png","3_black.png",
        "4_black.png","5_black.png","6_black.png",
        "7_black.png","8_black.png","9_black.png","blank.png"]))))
        self.nums_blu = list(map(pygame.image.load,
                        list(map(set_path,
        ["1_blue.png","2_blue.png","3_blue.png",
        "4_blue.png","5_blue.png","6_blue.png",
        "7_blue.png","8_blue.png","9_blue.png","blank.png"]))))

        #information from text board.
        self.initial_state = [["-"]*9 for i in range(9)]
        self.current_state = [["-"]*9 for i in range(9)]
        self.S = "123456789-"

        #information for selected grid.
        self.sel_grid_coord = []

    def set_from(self,display,state):
        self.initial_state = [[state[i][j] for j in range(9)] for i in range(9)]
        self.current_state = [[state[i][j] for j in range(9)] for i in range(9)]

    def update(self,display):
        display.blit(self.sudoku_board_image,(0,0))
        for i in range(9):
            for j in range(9):
                if self.initial_state[i][j]!="-":
                    display.blit(self.nums_blk[self.S.index(self.initial_state[i][j])],
        (((j//3+1)*self.thick_line_width+(j+1)*self.thin_line_width+j*self.small_grid_side),
        ((i//3+1)*self.thick_line_width+(i+1)*self.thin_line_width+i*self.small_grid_side), 
                         self.small_grid_side-2,self.small_grid_side-2))
                else:
                    display.blit(self.nums_blu[self.S.index(self.current_state[i][j])],
        (((j//3+1)*self.thick_line_width+(j+1)*self.thin_line_width+j*self.small_grid_side),
        ((i//3+1)*self.thick_line_width+(i+1)*self.thin_line_width+i*self.small_grid_side), 
                         self.small_grid_side-2,self.small_grid_side-2))

        if self.sel_grid_coord :
            i,j= self.sel_grid_coord
            if self.initial_state[j][i]=="-":
                col = (0,255,0)
            else:
                col = (255,0,0)
            pygame.draw.rect(display,col,
        (((i//3+1)*self.thick_line_width+(i+1)*self.thin_line_width+i*self.small_grid_side)-1,
         ((j//3+1)*self.thick_line_width+(j+1)*self.thin_line_width+j*self.small_grid_side)-1,
                         self.small_grid_side,self.small_grid_side),3)
        
    def index_select_grid(self,i,j):
        if i in range(9) and j in range(9):
            self.sel_grid_coord = [i,j]
            return True
        return False
    def mouse_select_grid(self,x,y):
        i = (x-self.thin_line_width-self.thick_line_width)//(self.small_grid_side+self.thin_line_width+self.thick_line_width//3)
        j = (y-self.thin_line_width-self.thick_line_width)//(self.small_grid_side+self.thin_line_width+self.thick_line_width//3)
        return self.index_select_grid(i,j)
        
    
    def key_select_grid(self,up,down,right,left):
        if self.sel_grid_coord:
            i,j = self.sel_grid_coord
            if up==1 and down==0 and right==0 and left==0:
                j = (j-1)%9
            elif up==0 and down==1 and right==0 and left==0:
                j = (j+1)%9
            elif up==0 and down==0 and right==0 and left==1:
                i = (i-1)%9
            elif up==0 and down==0 and right==1 and left==0:
                i = (i+1)%9
            return self.index_select_grid(i,j)
        else:
            return self.index_select_grid(0,0)
    
    def change_sel_grid(self,v):
        if self.sel_grid_coord:
            i,j = self.sel_grid_coord
            if self.initial_state[j][i]=="-":
                self.current_state[j][i]=v
            

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
display_width = 359
display_height = 400
display = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Sudoku')


clock = pygame.time.Clock()
run = True
solve = False
ss = sudoku.sudoku_solver(M,is_pausable=True)
reset = False

display.fill((255,255,255))

B = board("assets")
B.set_from(display,M)

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
        if key_press[pygame.K_SPACE]==1:
            solve = True
        elif key_press[pygame.K_r]==1:
            reset = True
        if not (solve or reset):
            if click[0]==1:
                B.mouse_select_grid(mouse[0],mouse[1])
            if i==-1:
                B.key_select_grid(key_press[pygame.K_UP],key_press[pygame.K_DOWN],
                                  key_press[pygame.K_RIGHT],key_press[pygame.K_LEFT])
            else:
                B.change_sel_grid(B.S[i])
    if solve:
        q = next(ss)
        if not(q==1 or q==-1):
            B.index_select_grid(q[1],q[0])
            B.change_sel_grid(q[2])
        else:
            solve = False
            M = [[B.initial_state[i][j] for j in range(9)]for i in range(9)]
            ss = sudoku.sudoku_solver(M,is_pausable=True)
    elif reset:
        M = [[B.initial_state[i][j] for j in range(9)]for i in range(9)]
        B.set_from(display,M)
        ss = sudoku.sudoku_solver(M,is_pausable=True)
        reset = False

    B.update(display)
    pygame.display.update()
    clock.tick(60)

pygame.quit()

    
    
