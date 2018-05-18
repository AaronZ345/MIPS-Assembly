#baseAddr 00000000
l:
ADD $t8,$s3,$v0;
sub $s1,$t1,$t2;
addi $t0,$zero,1000;
sw $t0,50($t3);
lw $s7,50($t3);
and $t1,$t2,$t3;
or $a1,$a2,$a3;
move $t1,$t0;
sll $t0,$t0,5;
srl $s5,$s7,5;
beq $t0,$s6,l;
bne $t2,$s7,p;
slt $s0,$s1,$s2;
nor $t1,$t0,$t3;
bge $t1,$t0,l;
blt $s3,$s2,p;

p:
slt $gp,$sp,$fp;
xor $t0,$t1,$t0;
jal 1000;
j 2000;
jr $ra;

Exit: