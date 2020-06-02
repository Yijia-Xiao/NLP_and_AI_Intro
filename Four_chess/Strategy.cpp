#include "Point.h"
#include "Strategy.h"
#include "Judge.h"

#include <iostream>
#include <stdio.h>
#include <time.h>
#include <random>
#include <string>
#include <cstring>
#include <cmath>
#include <cstdio>

using namespace std;

#define MAX_NODES 8000000
#define MAX_COL 12

int virttop[MAX_COL];
int **virtboard;
int nox, noy, m, n;

struct Node
{
	int father, l, r;
	int value, vis, reward;
	int x, y;
	int user;
	Node()
	{
		father = 0;
		l = -1, r = 0;
		value = vis = x = y = user = 0;
	}
} nodes[MAX_NODES];

void place(int x, int y, int userid)
{
	virtboard[x][y] = userid;
	// No.y column will have 1 less position avaliable
	virttop[y]--;
	if (y == noy && (virttop[y] == nox + 1))
		virttop[y]--;
}

int rewardvalue(int x, int y, int userid)
{
	if (machineWin(x, y, m, n, virtboard) && userid == 2)
		return 1;
	else if (userWin(x, y, m, n, virtboard) && userid == 1)
		return -1;
	else if (isTie(n, virttop))
		return 0;
	return -100;
}

int select(int idx)
{
	double optim = -100000000, uc = 0, value = 0;
	int resid = -1;
	for (int i = nodes[idx].l; i <= nodes[idx].r; i++)
	{
		value = (nodes[idx].user == 1) ? nodes[i].value : -nodes[i].value;
		uc = (double(value + 1.0) / (nodes[i].vis)) + 0.8 * sqrt(2 * log(nodes[nodes[i].father].vis) / (nodes[i].vis));
		if (uc > optim || resid == -1)
			optim = uc, resid = i;
	}
	place(nodes[resid].x, nodes[resid].y, nodes[resid].user);
	return resid;
}

void expand(int idx, int userid, int father, int col)
{
	nodes[idx].l = -1, nodes[idx].r = 0, nodes[idx].value = 0, nodes[idx].vis = 0, nodes[idx].reward = -100;
	nodes[idx].father = father, nodes[idx].user = userid;
	nodes[idx].x = virttop[col] - 1, nodes[idx].y = col;
}

void backprop(int &now, int &root, int &reward)
{
	while (now != root)
	{
		nodes[now].value += reward;
		nodes[now].vis++;
		now = nodes[now].father;
	}
	if (now == root)
	{
		nodes[now].value += reward;
		nodes[now].vis++;
	}
}
int policy()
{
	// when we reached the time limit,
	// find the best state node to go
	// we donnot use the original evaluation function, because the root node doesn't have father node
	double b = -1e6, ucb = 0;
	int ans = -1;
	for (int i = nodes[0].l; i <= nodes[0].r; i++)
	{
		ucb = double(nodes[i].value) / double(nodes[i].vis);
		if (ucb > b || ans == -1)
			ans = i, b = ucb;
	}
	return ans;
}

extern "C" Point *getPoint(const int M, const int N, const int *top, const int *_board,
						   const int lastX, const int lastY, const int noX, const int noY)
{
	clock_t start = clock();
	int x = -1, y = -1;
	int **board = new int *[M];
	for (int i = 0; i < M; i++)
	{
		board[i] = new int[N];
		for (int j = 0; j < N; j++)
		{
			board[i][j] = _board[i * N + j];
		}
	}

	int nodecnt = 0;
	m = M, n = N, nox = noX, noy = noY;
	virtboard = new int *[M];
	for (int i = 0; i < M; i++)
		virtboard[i] = new int[N];

	// every turn, we need to reinit the board
	// initialize
	memset(nodes, 0, sizeof(nodes));
	nodes[0].user = 1, nodes[0].l = -1, nodes[0].r = 0, nodes[0].reward = -100;

	// each epoch is another round of simulation
	while (true)
	{
		if ((double)(clock() - start) / double(CLOCKS_PER_SEC) > 2.8)
			break;

		for (int i = 0; i < M; i++)
			for (int j = 0; j < N; j++)
				virtboard[i][j] = board[i][j];
		for (int i = 0; i < N; i++)
			virttop[i] = top[i];

		int root = 0, now = 0;
		while (nodes[now].l != -1)
			now = select(now);

		if (!nodes[now].vis)
			nodes[now].reward = rewardvalue(nodes[now].x, nodes[now].y, nodes[now].user);

		// the result hasn't been determined
		if (nodes[now].reward == -100)
		{
			nodes[now].l = nodecnt + 1;
			for (int i = 0; i < N; i++)
			{
				if (virttop[i] > 0)
				{
					// if expandable, we expand No.i column
					nodecnt++;
					expand(nodecnt, 3 - nodes[now].user, now, i);
				}
			}
			// right idx included
			nodes[now].r = nodecnt;

			int randson = (rand() % (nodes[now].r - nodes[now].l + 1)) + nodes[now].l;
			now = randson;
			// playchess(randson);
			place(nodes[randson].x, nodes[randson].y, nodes[randson].user);
			int r = rewardvalue(nodes[randson].x, nodes[randson].y, nodes[randson].user);
			nodes[randson].reward = r;
			int u = nodes[now].user;
			// stimulation
			// search until win/lose
			while (r == -100)
			{
				int col = rand() % n;
				// no more place for chessman
				while (virttop[col] == 0)
					col = rand() % n;
				int row = virttop[col] - 1;
				place(row, col, u);
				r = rewardvalue(row, col, u);
				u = 3 - u;
			}
			// BP
			backprop(now, root, r);
		}
		// result of current node can be determined
		else
			backprop(now, root, nodes[now].reward);
	}

	int id = policy();
	x = nodes[id].x;
	y = nodes[id].y;
	clearArray(M, N, virtboard);
	clearArray(M, N, board);
	return new Point(x, y);
}

extern "C" void clearPoint(Point *p)
{
	delete p;
	return;
}

void clearArray(int M, int N, int **board)
{
	for (int i = 0; i < M; i++)
	{
		delete[] board[i];
	}
	delete[] board;
}
