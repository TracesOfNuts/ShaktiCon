![challenge](.\img\Capture.PNG)

#### CHALLENGE INFORMATION

Let's compare!

Author: bl4ck_Widw

#### FILES

[firmware](./src/hack)

---

#### (Solution) hack

Running the file:

```
$ ./src/hack
Enter the string:
```

Enter some random input:

```
Enter the string: this_is_some_random_input
```

Output:

```
I dont think so XD
```

Since this is a 'reversing' challenge, we probably need to use GDB.

First, let's check the file type on the binary:

```
$ ./src/hack: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 3.2.0, BuildID[sha1]=957c3059af2115499018a7fb5dc42e3ae3bf20f2, not stripped
```

This shows that the binary is not stripped. When a program is compiled, the compiler adds extra information to the binary called debugging symbols. These symbols makes it easier to debug a program. A stripped binary is a program that is compiled with a *strip* flag that tells the compiler to discard these debugging symbols and compile to program as it is. As this is not stripped, we can use symbols to debug.

Let's open the file using GDB.

```
$ gdb ./src/firmware
```

The first logical step would be to find the entry point. Since it is not stripped, we can directly access the "main" function.

```
gdb-peda$ break main
Breakpoint 1 at 0x7fe
```

The next step is to run the program so that we can disassemble it.

```
Starting program: /mnt/d/CTF/2021/ShaktiCon/Reversing/hack/src/hack
[----------------------------------registers-----------------------------------]
RAX: 0x80007fa --> 0x30ec8348e5894855
RBX: 0x0
RCX: 0x7fffff79e718 --> 0x7fffff7a0b00 --> 0x0
RDX: 0x7ffffffee208
RSI: 0x7ffffffee1f8
RDI: 0x1
RBP: 0x7ffffffee100
RSP: 0x7ffffffee100
RIP: 0x80007fe --> 0x48b486430ec8348
R8 : 0x0
R9 : 0x7fffff7d0180 --> 0x56415741e5894855
R10: 0x5
R11: 0x0
R12: 0x80006f0 --> 0x89485ed18949ed31
R13: 0x0
R14: 0x0
R15: 0x0
EFLAGS: 0x246 (carry PARITY adjust ZERO sign trap INTERRUPT direction overflow)
[-------------------------------------code-------------------------------------]
   0x80007f5 <frame_dummy+5>:   jmp    0x8000760 <register_tm_clones>
   0x80007fa <main>:    push   rbp
   0x80007fb <main+1>:  mov    rbp,rsp
=> 0x80007fe <main+4>:  sub    rsp,0x30
   0x8000802 <main+8>:  mov    rax,QWORD PTR fs:0x28
   0x800080b <main+17>: mov    QWORD PTR [rbp-0x8],rax
   0x800080f <main+21>: xor    eax,eax
   0x8000811 <main+23>: lea    rdi,[rip+0x17c]        # 0x8000994
[------------------------------------stack-------------------------------------]
Invalid $SP address: 0x7ffffffee100
[------------------------------------------------------------------------------]
Legend: code, data, rodata, value

Breakpoint 1, 0x00000000080007fe in main ()
```

Great. Let's disassemble this region:

```
gdb-peda$ disassemble
Dump of assembler code for function main:
   0x00000000080007fa <+0>:     push   rbp
   0x00000000080007fb <+1>:     mov    rbp,rsp
=> 0x00000000080007fe <+4>:     sub    rsp,0x30
   0x0000000008000802 <+8>:     mov    rax,QWORD PTR fs:0x28
   0x000000000800080b <+17>:    mov    QWORD PTR [rbp-0x8],rax
   0x000000000800080f <+21>:    xor    eax,eax
   0x0000000008000811 <+23>:    lea    rdi,[rip+0x17c]        # 0x8000994
   0x0000000008000818 <+30>:    mov    eax,0x0
   0x000000000800081d <+35>:    call   0x80006b0 <printf@plt>
   0x0000000008000822 <+40>:    lea    rax,[rbp-0x20]
   0x0000000008000826 <+44>:    mov    rsi,rax
   0x0000000008000829 <+47>:    lea    rdi,[rip+0x177]        # 0x80009a7
   0x0000000008000830 <+54>:    mov    eax,0x0
   0x0000000008000835 <+59>:    call   0x80006c0 <__isoc99_scanf@plt>
   0x000000000800083a <+64>:    mov    DWORD PTR [rbp-0x28],0x1
   0x0000000008000841 <+71>:    lea    rax,[rbp-0x20]
   0x0000000008000845 <+75>:    mov    rdi,rax
   0x0000000008000848 <+78>:    call   0x8000690 <strlen@plt>
   0x000000000800084d <+83>:    cmp    rax,0x10
   0x0000000008000851 <+87>:    je     0x8000869 <main+111>
   0x0000000008000853 <+89>:    lea    rdi,[rip+0x150]        # 0x80009aa
   0x000000000800085a <+96>:    call   0x8000680 <puts@plt>
   0x000000000800085f <+101>:   mov    edi,0x0
   0x0000000008000864 <+106>:   call   0x80006d0 <exit@plt>
   0x0000000008000869 <+111>:   mov    DWORD PTR [rbp-0x24],0x0
   0x0000000008000870 <+118>:   jmp    0x80008ba <main+192>
   0x0000000008000872 <+120>:   mov    eax,DWORD PTR [rbp-0x24]
   0x0000000008000875 <+123>:   cdqe
   0x0000000008000877 <+125>:   movzx  edx,BYTE PTR [rbp+rax*1-0x20]
   0x000000000800087c <+130>:   mov    eax,DWORD PTR [rbp-0x24]
   0x000000000800087f <+133>:   add    eax,0x3
   0x0000000008000882 <+136>:   cdqe
   0x0000000008000884 <+138>:   lea    rcx,[rax*4+0x0]
   0x000000000800088c <+146>:   lea    rax,[rip+0x20078d]        # 0x8201020 <v2>
   0x0000000008000893 <+153>:   mov    eax,DWORD PTR [rcx+rax*1]
   0x0000000008000896 <+156>:   cmp    dl,al
   0x0000000008000898 <+158>:   jne    0x80008a0 <main+166>
   0x000000000800089a <+160>:   add    DWORD PTR [rbp-0x28],0x1
   0x000000000800089e <+164>:   jmp    0x80008b6 <main+188>
   0x00000000080008a0 <+166>:   lea    rdi,[rip+0x116]        # 0x80009bd
   0x00000000080008a7 <+173>:   call   0x8000680 <puts@plt>
   0x00000000080008ac <+178>:   mov    edi,0x0
   0x00000000080008b1 <+183>:   call   0x80006d0 <exit@plt>
   0x00000000080008b6 <+188>:   add    DWORD PTR [rbp-0x24],0x1
   0x00000000080008ba <+192>:   mov    eax,DWORD PTR [rbp-0x24]
   0x00000000080008bd <+195>:   cdqe
   0x00000000080008bf <+197>:   movzx  eax,BYTE PTR [rbp+rax*1-0x20]
   0x00000000080008c4 <+202>:   test   al,al
   0x00000000080008c6 <+204>:   jne    0x8000872 <main+120>
   0x00000000080008c8 <+206>:   cmp    DWORD PTR [rbp-0x28],0x11
   0x00000000080008cc <+210>:   jne    0x80008e6 <main+236>
   0x00000000080008ce <+212>:   lea    rax,[rbp-0x20]
   0x00000000080008d2 <+216>:   mov    rsi,rax
   0x00000000080008d5 <+219>:   lea    rdi,[rip+0xe6]        # 0x80009c2
   0x00000000080008dc <+226>:   mov    eax,0x0
   0x00000000080008e1 <+231>:   call   0x80006b0 <printf@plt>
   0x00000000080008e6 <+236>:   mov    eax,0x0
   0x00000000080008eb <+241>:   mov    rdx,QWORD PTR [rbp-0x8]
   0x00000000080008ef <+245>:   xor    rdx,QWORD PTR fs:0x28
   0x00000000080008f8 <+254>:   je     0x80008ff <main+261>
   0x00000000080008fa <+256>:   call   0x80006a0 <__stack_chk_fail@plt>
   0x00000000080008ff <+261>:   leave
   0x0000000008000900 <+262>:   ret
End of assembler dump.
```

This is the part where we have to do some trial and error.

For the first run, we shall step through each instruction using the command: `ni` and observe the output of the program until it ends.

We noticed the following:

- at `0x8000835`, the program prints: `Enter the string:`

  - ```
    [-------------------------------------code-------------------------------------]
       0x8000826 <main+44>: mov    rsi,rax
       0x8000829 <main+47>: lea    rdi,[rip+0x177]        # 0x80009a7
       0x8000830 <main+54>: mov    eax,0x0
    => 0x8000835 <main+59>: call   0x80006c0 <__isoc99_scanf@plt>
       0x800083a <main+64>: mov    DWORD PTR [rbp-0x28],0x1
       0x8000841 <main+71>: lea    rax,[rbp-0x20]
       0x8000845 <main+75>: mov    rdi,rax
       0x8000848 <main+78>: call   0x8000690 <strlen@plt>
    Guessed arguments:
    arg[0]: 0x80009a7 --> 0x6e6f642049007325 ('%s')
    arg[1]: 0x7ffffffee0e0
    ```

  - This is the same as when we tried running the program at the very start.

  - The user input will be stored in `0x7ffffffee0e0`. Note that this will be useful later.

  - You can input any random input here. For the sake of demonstration, I used the same as the shown at the start i.e. `this_is_some_random_input`

- at `0x8000848`, the program calls a `strlen` function

  - ```
    [-------------------------------------code-------------------------------------]
       0x800083a <main+64>: mov    DWORD PTR [rbp-0x28],0x1
       0x8000841 <main+71>: lea    rax,[rbp-0x20]
       0x8000845 <main+75>: mov    rdi,rax
    => 0x8000848 <main+78>: call   0x8000690 <strlen@plt>
       0x800084d <main+83>: cmp    rax,0x10
       0x8000851 <main+87>: je     0x8000869 <main+111>
       0x8000853 <main+89>: lea    rdi,[rip+0x150]        # 0x80009aa
       0x800085a <main+96>: call   0x8000680 <puts@plt>
    Guessed arguments:
    arg[0]: 0x7ffffffee0e0
    ```

  - This function just returns the length of C string.

  - Here we can see that the argument for this function is also `0x7ffffffee0e0`. 

- at `0x800084d`, the program does a comparison instruction followed by a `je` instruction.

  - ```0x800084d <main+83>: cmp    rax,0x1
    0x800084d <main+83>: cmp    rax,0x10
    0x8000851 <main+87>: je     0x8000869 <main+111>
    ```

  - This basically compares the value within the `rax` register with the hex value `0x10`. And goes to the respective instruction depending on the comparison value. 

  - Note that at this stage, `rax` is holding the value `0x1`

- Since our input is `rax` is not equal to `0x10`, it proceeded to the next instruction

  -  `0x8000853 <main+89>: lea    rdi,[rip+0x150]        # 0x80009aa`

- Continuing stepping through the program gives us the "I dont think so XD" message and finally terminates.

Based on the observations above, we can re-run the steps above but with some modifications.

Let's step through until `0x800084d` i.e. at the comparison instruction.

We can modify the `rax` value at runtime and step through the program.

```
gdb-peda$ set $rax=0x10
gdb-peda$ info registers
rax            0x10                0x10
rbx            0x0                 0x0
rcx            0x20                0x20
rdx            0x7ffffffee0e0      0x7ffffffee0e0
rsi            0xa                 0xa
rdi            0x7ffffffee0e0      0x7ffffffee0e0
rbp            0x7ffffffee100      0x7ffffffee100
rsp            0x7ffffffee0d0      0x7ffffffee0d0
r8             0x0                 0x0
r9             0xffffffffffffff80  0xffffffffffffff80
r10            0x7fffff7523c0      0x7fffff7523c0
r11            0x6f                0x6f
r12            0x80006f0           0x80006f0
r13            0x0                 0x0
r14            0x0                 0x0
r15            0x0                 0x0
rip            0x800084d           0x800084d <main+83>
eflags         0x202               [ IF ]
cs             0x33                0x33
ss             0x2b                0x2b
ds             0x0                 0x0
es             0x0                 0x0
fs             0x0                 0x0
gs             0x0                 0x0
```

Now that `rax` has been changed, we can continue stepping through and see the difference.

We observe at `0x8000896`, there is another comparison.

- This time it is `dl` with `al` (i.e. least significant bit of `rdx` and `rax` respectively)
- `al` is holding the value `_`
- and it seems like `dl` is dependent on the input (you can confirm this by changing the user input string and observing the change in the `rdx` register)

Continuing the program will print `Nope` and finally terminate.

Let's repeat all the above, but this time changing the `dl` value to `_` before the `0x8000896` comparison. For the sake of not making this document too wordy, I will skip the steps to do this as this is similar to the steps taken earlier. If you are not able to follow through, refer to the previous instructions or you may message me personally.

Once, we have changed the `dl` value to `_`, we shall step through until we see the another comparison at `0x80008c4` followed by a `jne` instruction.

If we follow through, the program will repeat the instruction at `0x8000896` however, this time `al` is holding `H` instead. 

We shall continue the program and taking note of the `rdx` values when with the `rax` values. This gets us the flag.

Flag:

```
shaktictf{__H4cK_tH3_M00n_}
```

---

#### References

- [Finding main() in Stripped Binary - bin 0x2C (YouTube)](https://www.youtube.com/watch?v=N1US3c6CpSw)
- [Reversing and Cracking first simple Program - bin 0x05 (YouTube)](https://www.youtube.com/watch?v=VroEiMOJPm8)
- [GDB Quick Reference](https://users.ece.utexas.edu/~adnan/gdb-refcard.pdf)
- [Working With Stripped Binaries in GDB](https://medium.com/@tr0id/working-with-stripped-binaries-in-gdb-cacacd7d5a33)
- [x86 (Wikipedia)](https://en.wikipedia.org/wiki/X86)
