SIZE = 640  # size of the grid displayed on screen
BLOCKS_EACH_LINE = 80  # number of blocks on each line
BLOCK_WIDTH = SIZE // BLOCKS_EACH_LINE  # width of each block
HALF_WIDTH = BLOCK_WIDTH // 2  # 1/2 width of each block
WIN_W = SIZE + 330  # width of the screen (extra 330 for text)
WIN_H = SIZE  # height of the screen

START_POS = (6, 6)  # index for start block
END_POS = (BLOCKS_EACH_LINE - 7, BLOCKS_EACH_LINE - 7)  # index for end block
