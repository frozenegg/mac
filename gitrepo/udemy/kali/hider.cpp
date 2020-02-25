void hide(){
  HWND stealth;
  AllocConsole();
  stealth=FindWindowA("ConsoleWindowClass", NULL);
  ShowWindow(stealth, 0);
}
