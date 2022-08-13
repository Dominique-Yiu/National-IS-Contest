#include <iostream>
#include <windows.h>
using namespace std;
void setCpuUse(int use)
{
	int workTime = use;
	int idleTime = 100- workTime;
	DWORD startTime;
	while (1)
	{
		startTime = GetTickCount();
		while (GetTickCount() - startTime <= workTime);
		Sleep(idleTime);
	}
}

int main()
{
	SetThreadAffinityMask(GetCurrentThread(), 6);
	setCpuUse(20);
	return 0;
}
