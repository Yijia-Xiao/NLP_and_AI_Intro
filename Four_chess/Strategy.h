#ifndef STRATEGY_H_
#define STRATEGY_H_

#include "Point.h"

extern "C" Point *getPoint(const int M, const int N, const int *top, const int *_board,
						   const int lastX, const int lastY, const int noX, const int noY);

extern "C" void clearPoint(Point *p);

void clearArray(int M, int N, int **board);

int select(int idx);
void place(int x, int y, int userid);
int rewardvalue(int x, int y, int userid);
void expand(int idx, int userid, int father, int col);
int policy();
void backprop(int &now, int &root, int &reward);
#endif
