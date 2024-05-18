# Co_Project

we have made 5 functions 
1) ado (opcode : 10101); Type C; add one to the source register and storing the final data in destination register; ado reg1 reg2;
   reg1 is destination register where the final data stored; reg2 is source register from where data is taken
   
   ado reg1 reg2;
   10101_00000_001_010;
   in this case data of reg2 is taken(let it be x), then (x+1) is stored in reg1  
   
   

2) adt (opcode : 10110); Type C; add two to the source register and storing the final data in destination register; adt reg1 reg2;
   reg1 is destination register where the final data stored; reg2 is source register from where data is taken.
   
   adt reg1 reg2;
   10110_00000_001_010;
   in this case data of reg2 is taken(let it be x), then (x+2) is stored in reg1  
   
   
3) hlf (opcode : 10111); Type C; it divides the data of source register by two and stores at destination register; hlf reg1 reg2;
   reg1 is destination register where the final data stored; reg2 is source register from where data is taken.
   
   hlf reg1 reg2;
   10111_00000_001_010;
   in this case data of reg2 is taken(let it be x), then (x/2) is stored in reg1  
   

4) sbo (opcode : 10011); Type C; Subtracts one from the source register and storing the final data in destination register; sbo reg1 reg2;
   reg1 is destination register where the final data stored; reg2 is source register from where data is taken.
   
   sbo reg1 reg2;
   10011_00000_001_010;
   in this case data of reg2 is taken(let it be x), then (x-1) is stored in reg1  
   
   
5) mpt (opcode : 10100); Type C; it multiply the data of source register by two and stores at destination register; mpt reg1 reg2;
   reg1 is destination register where the final data stored; reg2 is source register from where data is taken.
   
   mpt reg1 reg2;
   10100_00000_001_010;
   in this case data of reg2 is taken(let it be x), then (x*2) is stored in reg1  
