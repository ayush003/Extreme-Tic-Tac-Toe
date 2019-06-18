//By : Ayush Singhania

#include<bits/stdc++.h>
using namespace std;
typedef long long int ll;
#define fast_IO ios::sync_with_stdio(false);cin.tie(NULL);cout.tie(NULL);
char board[5][5];
string name;

bool game_continue(){
	for(int i=0;i<3;i++)
		for(int j=0;j<3;j++)
			if(board[i][j]=='_') return true;
	return false;
}


int function()
{
	// Checking for Rows for X or O victory.
	for(int row = 0; row<3; row++)
	{
		if (board[row][0]==board[row][1] && board[row][1]==board[row][2])
		{
			if (board[row][0]=='x')
				return +100;
			else if (board[row][0]==name[0])
				return -100;
		}
	}
	// Checking for Columns for X or O victory.
	for (int col = 0; col<3; col++)
	{
		if (board[0][col]==board[1][col] && board[1][col]==board[2][col])
		{
			if (board[0][col]=='x')
				return +100;

			else if (board[0][col]==name[0])
				return -100;
		}
	}
	// Checking for Diagonals for X or O victory.
	if (board[0][0]==board[1][1] && board[1][1]==board[2][2])
	{
		if (board[0][0]=='x')
			return +100;
		else if (board[0][0]==name[0])
			return -100;
	}

	if (board[0][2]==board[1][1] && board[1][1]==board[2][0])
	{
		if (board[0][2]=='x')
			return +100;
		else if (board[0][2]==name[0])
			return -100;
	}

	// Else if none of them have won then return 0
	return 0;
}

void board_print(){
	for(int i=0;i<3;i++)
	{	
		cout<<endl;
		for(int j=0;j<3;j++)
			cout<<board[i][j]<<" ";
		cout<<" | ";
		for(int j=0;j<3;j++)
			cout<<"("<<i+1<<","<<j+1<<")";

		cout<<endl;
	}
	cout<<endl;
}

int minmax(int depth,bool Is){

	int points=function();
	if(points== +100 || points== -100 )
		return points;
	if(any_move_remaining()==false)
		return false;

	if (Is)
	{
		int best = -10000000;
		// Traverse all cells
		for (int i = 0; i<3; i++)
		{
			for (int j = 0; j<3; j++)
			{
				// Check if cell is empty
				if (board[i][j]=='_')
				{
					// Make the move
					board[i][j] = 'x';
					// Call minimax recursively and choose
					// the maximum value
					best = max( best,
							minmax( depth+1, !Is) );

					// Undo the move
					board[i][j] = '_';
				}
			}
		}
		return best;
	}

	// If this minimizer's move
	else
	{
		int best = 1000;
		// Traverse all cells
		for (int i = 0; i<3; i++)
		{
			for (int j = 0; j<3; j++)
			{
				// Check if cell is empty
				if (board[i][j]=='_')
				{
					// Make the move
					board[i][j] = name[0];
					// Call minimax recursively and choose
					// the minimum value
					best = min(best,minmax(depth+1, !Is));
					// Undo the move
					board[i][j] = '_';
				}
			}
		}
		return best;
	}
}

void best_move(){
	int X=-1,Y=-1,BEST=-1;

	for(int i=0;i<3;i++)
		for(int j=0;j<3;j++)
		{
			if(board[i][j]=='_')
			{
				board[i][j]='x';
				int Val = minmax(0,false);
				board[i][j]='_';

				if(Val>BEST){
					X=i,Y=j,BEST=Val;
				}
			}

		}

	cout<<"Bot's Move :  "<<X+1<<"  "<< Y+1<<endl;

	board[X][Y]='x';
}


int main()
{
	for(int i=0;i<3;i++)
		for(int j=0;j<3;j++)
			board[i][j]='_';
				// name[0] = user
				// x = bot 

	cout<<"ENTER YOUR NAME : "<<endl;
	cin>>name;
	cout<<endl;
	cout<<" FIRST LETTER OF YOUR NAME DENOTES YOUR PLAYER "<<endl;
	cout<<endl;
	cout<<" X DENOTES SYSTEMS PLAYER "<<endl;
	cout<<endl;
	cout<<"FIRST TURN IS YOURS "<<endl;
		board_print();
	while(function()==false && game_continue()){
		int x,y;

		// player movers
		int correct_input=false;
		do{

		cout<<name<<"'s  Move : ";
		cin>>x>>y;
		x--,y--;
		if(board[x][y]=='_')
		{
			correct_input=true;
			board[x][y]=name[0];
		}
		else continue;

		}while(correct_input==false);
		if(function()) break;
		else  board_print();

		// bot moves
		best_move();
		if(function()) break;
		else  board_print();

	}

	if(function()== -100)
	{
		cout<<endl;
		cout<<endl;
		cout<<name<<"       WINS !!!! "<<endl;
		board_print();
		cout<<"      G A M E     O V E R    "<<endl;

	}
	else if(function()== 100)
	{
		cout<<endl;
		cout<<endl;
		cout<<"           BOT WINS !!!! "<<endl;
		board_print();
		cout<<"      G A M E     O V E R    "<<endl;
	}
	else{
		cout<<endl;
		cout<<endl;
		cout<<"TIE !!!!"<<endl;
		board_print();
		cout<<"      G A M E     O V E R    "<<endl;

	}
	return 0;
}
