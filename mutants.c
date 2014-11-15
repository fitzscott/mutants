/* Attack of the Mutants!               Fitz Bushnell, June 1990 */
/* Attack of the Mutants is a boardgame, based loosely on Yaquinto's old */
/* game of the same name.  it, in turn, is inspired by innumerable bad */
/* 50's science fiction movies.  the mutants created by (disaster of your */
/* choice: nuclear war, comet/meteor strike, chemical weapons, etc.) attack */
/* a scientific outpost, manned by an absent-minded professor, his daughter */
/* and her dumb hubby, and his (the prof's, natch) cute gun-toting robots. */

#include stdio
#include curses
#include string
#include time
#include processes

#define debug 0
#define debug2 0
#define debug3 0
#define num_equip 10            /* number of pieces of equipment */
#define num_robots 5            /* number of robots */
#define num_mutants 50          /* number of mutants */
#define num_doors 39            /* number of doors */
#define Nothing_l list+0        /* equipment offsets in array */
#define Rifle_l list+1
#define Pipe_l list+2
#define Chair_l list+3
#define Pistol_l list+4
#define Axe_l list+5
#define Extinguisher_l list+6
#define Secret_Weapon_l list+7
#define Slide_Rule_l list+8
#define Spare_Parts_l list+9

WINDOW *messes;

/* Setup section - decide really basic stuff, like data structures, */
/* piece values & placement, equipment, etc. */

struct equip_list               /* what sort of weapons, etc.  will be */
  {                             /* lying around. */
    char item[15];              /* what it is */
    char image;                 /* what it looks like on screen */
    int attack_add;             /* whether it can be used as a club */
    int range_attack;           /* whether it can be fired */
    int distance;               /* how far it can be fired */
  } list[num_equip];

struct piece                    /* a struct defining the pieces */
  {
    char c_name[15];            /* string name of piece */
    char image;                 /* what they look like, e.g. robot='R' */
    int movement;               /* how many squares they can move */
    int xloc, yloc;             /* where they are currently */
    int hand_attack;            /* the h-t-h attack strength of the piece */
    int defense;                /* defense strength of piece */
    int hits;                   /* number of hit points */
    struct equip_list  *carried;   /* anything carried (1 thing each) */
  };

struct edge_squares             /* where the mutants will set up */
  {
    int xval;
    int yval;
  };

struct doors                    /* simple struct for doors */
  {
    int xloc, yloc;
  };

int seed;

int rndm()                      /* random # generator - don't like the */
				/* math function */
  {
    seed = seed % 201 * 17 + 16;
    return(seed);
  }

int dice(howmany)               /* generate 'howmany' 6-sided dice */
  int howmany;

  {
    int i, total = 0;

    for (i = 0; i < howmany; i++)
	total += (rndm() % 6 + 1);
    if (debug) printf("random total = %d ",total);
    return total;
  }

int checksquare(insquare)               /* check square to see if it's */
  char insquare;                        /* occupied. */

  {
    int i;

	/* it's empty, or it's a door - no problem */
    if ((insquare == ' ') || (insquare == '+')) return -1;
    for (i = 1; i <= num_equip; i++)
      if (insquare == list[i].image)    /* it's got an equipment item */
	  return i;
    return 0;                           /* else it's a wall or something */
  }

drawscreen()

  {
    FILE *map;                  /* pointer to the map file */
    char line[60];
    int i;

    if ((map = fopen("mutants.map","r")) == NULL)
      {
	fprintf(stderr,"Map file not found\n");
	exit(1);
      }
    for (i=0; i<19; i++)        /* put the map on-screen */
      {
	fgets(line,66,map);
	mvaddstr(i,1,line);
      }
    fclose(map);
    refresh();
  }

fixscreen()                     /* kludgey way to refresh screen */
				/* refresh doesn't seem to work */
  {
    WINDOW *nix;
    char msg[80];
    int i;

    for (i = 0; i < 80; i++) msg[i] = '#';
    nix = newwin(23,79,0,0);
    for (i = 0; i < 23; i++) mvwaddstr(nix,i,0,msg);
    wrefresh(nix);
    delwin(nix);
  }

assign(door)                    /* decide where doors will be */
  struct doors door[num_doors];

  {
    door[0].xloc = door[1].xloc = door[31].xloc 
		 = door[32].xloc = door[34].xloc = 1;
    door[2].xloc = door[3].xloc = door[4].xloc = door[30].xloc = 5;
    door[5].xloc = door[6].xloc = 6;
    door[9].xloc = door[10].xloc = 8;
    door[11].xloc = door[12].xloc = door[13].xloc = 12;
    door[14].xloc = door[15].xloc = 13;
    door[16].xloc = door[17].xloc = door[37].xloc = door[38].xloc = 14;
    door[18].xloc = door[19].xloc = door[20].xloc 
		  = door[33].xloc = door[35].xloc = 18;
    door[2].yloc = door[11].yloc = door[18].yloc = 17;
    door[3].yloc = door[12].yloc = door[19].yloc = 30;
    door[1].yloc = door[17].yloc = 55;
    door[5].yloc = door[14].yloc = 8;
    door[6].yloc = door[15].yloc = 58;
    door[10].yloc = door[16].yloc = 20;
    door[0].yloc = 29;
    door[4].yloc = door[7].yloc = 50;
    door[13].yloc = 49;
    door[20].yloc = door[37].yloc = 37;
    door[21].yloc = door[22].yloc = door[23].yloc = 52;
    door[24].yloc = door[25].yloc = door[26].yloc = 38;
    door[27].yloc = door[28].yloc = 36;
    door[29].yloc = door[9].yloc =  14;
    door[8].yloc = 15;
    door[33].yloc = 51;
    door[21].xloc = door[29].xloc = 4;
    door[22].xloc = door[25].xloc = door[27].xloc = door[36].xloc = 10;
    door[23].xloc = door[26].xloc = door[8].xloc = 15;
    door[28].xloc = door[31].yloc = 16;
    door[24].xloc = 3;
    door[7].xloc = 14;
    door[9].xloc = 11;
    door[30].yloc = door[35].yloc = 41;
    door[34].yloc = 39;
    door[32].yloc = 49;
    door[36].yloc = 45;
    door[38].yloc = 32;
  }

equipment()             /* stats for equipment to be found */

  {
    strcpy(list[0].item, "Nothing");    /* stats for nothing */
    list[0].image = ' ';
    list[0].attack_add = 0;
    list[0].range_attack = 0;
    list[0].distance = 0;
    strcpy(list[1].item, "Rifle");      /* stats for rifles */
    list[1].image = '>';
    list[1].attack_add = 2;
    list[1].range_attack = 7;
    list[1].distance = 10;
    strcpy(list[2].item, "Pipe");       /* stats for a metal club, basically */
    list[2].image = '|';
    list[2].attack_add = 3;
    list[2].range_attack = 0;
    list[2].distance = 0;
    strcpy(list[3].item, "Chair");      /* stats for a big wooden chair */
    list[3].image = '&';
    list[3].attack_add = 2;
    list[3].range_attack = 0;
    list[3].distance = 0;
    strcpy(list[4].item, "Pistol");     /* stats for a hand pistol */
    list[4].image = '=';
    list[4].attack_add = 1;
    list[4].range_attack = 6;
    list[4].distance = 8;
    strcpy(list[5].item, "Axe");        /* stats for an axe */
    list[5].image = 'x';
    list[5].attack_add = 6;
    list[5].range_attack = 0;
    list[5].distance = 0;
    strcpy(list[6].item, "Extinguisher");       /* fire extinguisher */
    list[6].image = '~';
    list[6].attack_add = 2;
    list[6].range_attack = 1;
    list[6].distance = 2;
    strcpy(list[7].item, "Secret Weapon");      /* secret weapon */
    list[7].image = '}';
    list[7].attack_add = 2;
    list[7].range_attack = 20;
    list[7].distance = 20;
    strcpy(list[8].item, "Slide Rule");         /* slide rule */
    list[8].image = ':';
    list[8].attack_add = 0;
    list[8].range_attack = 0;
    list[8].distance = 0;
    strcpy(list[9].item, "Spare Parts");        /* parts for construction */
    list[9].image = '$';
    list[9].attack_add = 1;
    list[9].range_attack = 0;
    list[9].distance = 0;
   }

place_player(chit)
  struct piece *chit;

  {
    int placex, placey, maxlim;
    char pcheck;

    maxlim = 0;
    do
      {
	placey = rndm() % 49 + 9;
	placex = rndm() % 15 + 3;
	pcheck = mvinch(placex,placey);
	if (++maxlim > 15)                      /* if we start to loop, */
	  {                                     /* play with the seed */
	    seed++;
	    maxlim = 0;
	  }
      }
    while (pcheck != ' ');
    chit->xloc = placex;
    chit->yloc = placey;
    setattr(_BOLD);
    mvaddch(chit->xloc,chit->yloc,chit->image);
    clrattr(_BOLD);
    refresh();
  }

place_mutants(mutant,lastmove)
  struct piece mutant[num_mutants];
  char lastmove[num_mutants];

  {
    int i, which;
    struct edge_squares square[142];
    char mcheck;

	/* initialize the edge squares, where the mutants set up */
    for (i = 7; i <= 59; i++)           /* first 106 squares */
      {
	square[i-7].xval = 0;
	square[i-7].yval = i;
	if (debug2) mvaddch(square[i-7].xval,square[i-7].yval,'.');
	square[i+46].xval = 19;
	square[i+46].yval = i;
	if (debug2) mvaddch(square[i+46].xval,square[i+46].yval,'.');
      }
    for (i = 1; i <= 18; i++)           /* last 36 squares */
      {
	square[i+105].xval = i;
	square[i+105].yval = 7;
	if (debug2) mvaddch(square[i+105].xval,square[i+105].yval,'.');
	square[i+123].xval = i;
	square[i+123].yval = 59;
	if (debug2) mvaddch(square[i+123].xval,square[i+123].yval,'.');
      }
    for (i = 0; i < num_mutants; i++)
      {
	/* choose a random square, from 0 to 142-i */
	which = rndm() % (142 - i);
	if (debug2) printf("which is %d ",which);
	mcheck = mvinch(square[which].xval,square[which].yval);
	if (mcheck == ' ')      /* don't put them on an occupied square */
	  {
	    mutant[i].xloc = square[which].xval;
	    mutant[i].yloc = square[which].yval;
	    if (mutant[i].xloc == 0)       lastmove[i] = 'j';
	    else if (mutant[i].xloc == 19) lastmove[i] = 'k';
	    else if (mutant[i].yloc == 7)  lastmove[i] = 'l';
	    else if (mutant[i].yloc == 59) lastmove[i] = 'h';
	  }
	else i--;
	/* get rid of chosen square, and bring in unchosen one */
	square[which].xval = square[141-i].xval;
	square[which].yval = square[141-i].yval;
	setattr(_BOLD);
	mvaddch(mutant[i].xloc,mutant[i].yloc,mutant[i].image);
	clrattr(_BOLD);
      }
  }

tell(msg, postclear)
  char *msg;
  int postclear;

  {

    wclear(messes);
    box(messes,'|','-');
    mvwaddstr(messes,1,1,msg);
    wrefresh(messes);
    if (postclear)
      {
	getch();
	wclear(messes);
	wrefresh(messes);
      }
  }

setup(prof, daughter, hero, computer, robot, mutant, lastmove, wave)
  struct piece *prof, *daughter, *hero, *computer;
  struct piece robot[num_robots], mutant[num_mutants];
  char lastmove[num_mutants];
  int wave;

  {
    int i, oft;

    /* ok, we need to decide the parameters on all the pieces. */
    /* we'll do the basics on the robots and the mutants first. */
    /* we'll decide where to set them up later - do it randomly */

    if (wave == 1) oft = num_mutants+1;
    if (wave == 2) oft = 4;
    if (wave == 3) oft = 3;
    if (wave == 1) for (i = 0; i < num_robots; i++)
      {
	strcpy(robot[i].c_name, "Robot");       /* robot stats */
	robot[i].image = 'R';
	robot[i].movement  = 4;
	robot[i].hand_attack = 1;
	robot[i].defense = 2;
	robot[i].hits = 2;
	robot[i].carried = Rifle_l;
      }
    for (i = 0; i < num_mutants; i++)           /* mutant stats */
      {
	if (! (i % oft))
	  {
	    strcpy(mutant[i].c_name,"Super Mutant");
	    mutant[i].image = 'S';
	    mutant[i].movement = wave+2;
	    mutant[i].hand_attack = 4;
	    mutant[i].defense = 1;
	    if (!(rndm() % 10))
	      {
		if (!(i % 3)) mutant[i].carried = Axe_l;
		else mutant[i].carried = Pipe_l;
	      }
	    else mutant[i].carried = Nothing_l;
	  }
	else
	  {
	    strcpy(mutant[i].c_name, "Mutant");
	    mutant[i].image = 'M';
	    mutant[i].movement = 2;
	    mutant[i].hand_attack = 3;
	    mutant[i].defense = 0;
	    mutant[i].carried = Nothing_l;
	  }
	mutant[i].hits = 3;
      }
	/* ok, now for the main characters' stuff: */
    if (wave == 1)
      {
	strcpy(prof->c_name, "Professor");
	prof->image = 'P';              /* the professor's stats */
	prof->movement = 4;
	prof->hand_attack = 2;
	prof->defense = 1;
	prof->hits = 2;
	prof->carried = Slide_Rule_l;
	strcpy(daughter->c_name, "Molly");
	daughter->image = 'D';          /* the daughter's stats */
	daughter->movement = 8;
	daughter->hand_attack = 2;
	daughter->defense = 2;
	daughter->hits = 3;
	daughter->carried = Nothing_l;
	strcpy(hero->c_name, "Bart");
	hero->image = 'H';                      /* the hero's stats */
	hero->movement = 7;
	hero->hand_attack = 4;
	hero->defense = 1;
	hero->hits = 4;
	hero->carried = Nothing_l;
	strcpy(computer->c_name, "BERT");
	computer->image = 'C';                  /* the computer's stats */
	computer->movement = 0;
	computer->hand_attack = 0;
	computer->defense = 2;
	computer->hits = 4;
	computer->carried = Nothing_l;
		/* ok, now for placement */
	place_player(prof);
	place_player(daughter);
	place_player(hero);
	for (i = 0; i < num_robots; i++)
	  place_player(robot+i);
	computer->xloc = 9;  computer->yloc = 32;
	setattr(_BOLD);
	mvaddch(computer->xloc,computer->yloc,computer->image);
	clrattr(_BOLD);
      }
    place_mutants(mutant,lastmove);
    refresh();
  }

/* Combat Section */
/* ok, we need an overall idea of how attacks are going to work.  */
/* there will be two sorts of attacks: hand-to-hand, and ranged. */
/* hand-to-hand is possible for anyone; ranged is possible if the */
/* character is carrying a ranged weapon such as a pistol.  the robots */
/* are assumed to have built-in rifles, although they are listed as */
/* being carried. */
/* once the attack phase starts, will put cursor on one unit, ask for */
/* a direction of attack, if any, for h-t-h.  then later, same procedure */
/* for ranged attack.  should allow either an h-t-h, or a ranged, not both */

int resolve(chit,pp,pd,ph,pc,robot,mutant,mode,target,curx,cury,min_dist,dist)
  struct piece chit;
  struct piece *pp,*pd,*ph,*pc,robot[num_robots],mutant[num_mutants];
  int mode;
  char target;
  int curx, cury;
  int min_dist,dist;
  
  /* resolve the combat between 'chit' and 'target'.  figure out exactly */
  /* who target is. */

  {
    int modifier, damage, dam_add, roll, j;
    struct piece *player_target;
    char msg[60];

    if (debug3) 
      {
	sprintf(msg,"dist = %d, min_dist = %d", dist, min_dist);
	tell(msg,1);
      }
    if (target == ' ') return 0;
    if ((target == '#') || (target == '+')) return -1;
    if ((target == 'M') || (target == 'S') || (target == 'Z'))  
      {                 /* attacking a mutant */
	if (dist < min_dist) return -3;                 /* if they're too */
		/* close, stop the attack and let 'em know */
	for (j=0; (((mutant[j].xloc != curx) ||          /* find out which */
		   (mutant[j].yloc != cury)) ||          /* mutant it is */
		   (mutant[j].hits <= 0)); j++); /* make sure it isn't dead */
	if (debug3)
	  {
	    sprintf(msg,"(attacking mutant %d)",j);
	    tell(msg,1);
	  }
	sprintf(msg,"%s, with %s, attacks a %s (hit key)",chit.c_name,
			chit.carried->item,mutant[j].c_name);
	tell(msg, 1);
	if (!mode)              /* hand attack */
	  {
	    modifier = chit.hand_attack - mutant[j].defense;
	    damage = chit.hand_attack + chit.carried->attack_add;
	  }
	else                    /* range attack */
	  {
		/* the further from the target, the harder it is to */
		/* hit and the less damage is done */
	    modifier = chit.carried->range_attack - 
		      (mutant[j].defense + 3*dist/4);
	    damage = chit.carried->range_attack - (dist / 2);
	  }
	roll = dice(2) + modifier;
	if (roll < 8) return -2;                /* need 8+ to hit */
	else if (roll == 8) dam_add = -3;
	else if (roll < 10) dam_add = -2;       /* the better the roll, */
	else if (roll < 12) dam_add = -1;       /* the better the damage */
	else dam_add = 0;
	if ((damage + dam_add) >= 0)
	  {                                     /* apply damage & evaluate */
	    mutant[j].hits -= (damage + dam_add);       
	    if (mutant[j].hits == 3) 
		sprintf(msg,"%s unhurt (hit key)",mutant[j].c_name);
	    else if (mutant[j].hits == 2) 
		sprintf(msg,"%s wounded (hit key)",mutant[j].c_name);
	    else if (mutant[j].hits == 1) 
		sprintf(msg,"%s badly hurt (hit key)",mutant[j].c_name);
	    else if (mutant[j].hits <= 0)  /* mutant is toast => remove it */
	      {
		sprintf(msg,"%s killed! (hit key)",mutant[j].c_name);
		/* drop anything the mutant was carrying */
		mvaddch(curx,cury,mutant[j].carried->image);
	      }
	  }
	else sprintf(msg,"The mutant shrugs it off (hit key)");
	tell(msg,1);
	return 1;
      }
    else if (target == 'R')             /* attacking a robot */
      {
	if (dist < min_dist) return -3;                 /* if they're too */
		/* close, stop the attack and let 'em know */
	for (j=0; (((robot[j].xloc != curx) ||          /* find out which */
		   (robot[j].yloc != cury)) ||         /* robot it is */
		   (robot[j].hits <= 0)); j++);  /* make sure it's functional */
	sprintf(msg,"%s, carrying %s, attacks the Robot (hit key)"
		,chit.c_name,chit.carried->item);
	tell(msg, 1);
	if (!mode)              /* hand attack */
	  {
	    modifier = chit.hand_attack - robot[j].defense;
	    damage = chit.hand_attack + chit.carried->attack_add;
	  }
	else                    /* range attack */
	  {
		/* the further from the target, the harder it is to */
		/* hit and the less damage is done */
	    modifier = chit.carried->range_attack - 
		      (robot[j].defense + 3*dist/4);
	    damage = chit.carried->range_attack - dist/2;
	  }
	roll = dice(2) + modifier;
	if (roll < 8) return -2;                /* need 8+ to hit */
	else if (roll == 8) dam_add = -3;
	else if (roll < 10) dam_add = -2;       /* the better the roll, */
	else if (roll < 12) dam_add = -1;       /* the better the damage */
	else dam_add = 0;
	if ((damage + dam_add) >= 0)
	  {
	    robot[j].hits -= (damage + dam_add);  /* apply damage & evaluate */
	    if (robot[j].hits == 2) 
		sprintf(msg,"Robot undamaged (hit key)");
	    else if (robot[j].hits == 1) 
		sprintf(msg,"Robot badly damaged (hit key)");
	    else                        /* robot is scrap => remove it */
	      {
		sprintf(msg,"Robot destroyed! (hit key)");
		mvaddch(curx,cury,robot[j].carried->image);
	      }
	  }
	else sprintf(msg,"The robot shrugs it off. (hit key)");
	tell(msg, 1);
	return 1;
      }
    else if ((target == 'P') || (target == 'D') || 
	     (target == 'H') || (target == 'C'))
      {                         /* attacking one of the characters */
	if (dist < min_dist) return -3;                 /* if they're too */
		/* close, stop the attack and let 'em know */
	if (target == 'P') player_target = pp;
	else if (target == 'D') player_target = pd;
	else if (target == 'H') player_target = ph;
	else if (target == 'C') player_target = pc;
	sprintf(msg,"%s, carrying %s, attacks %s (hit key)",
		chit.c_name, chit.carried->item, player_target->c_name);
	tell(msg, 1);
	if (!mode)              /* hand attack */
	  {
	    modifier = chit.hand_attack - player_target->defense;
	    damage = chit.hand_attack + chit.carried->attack_add;
	  }
	else                    /* range attack */
	  {
		/* the further from the target, the harder it is to */
		/* hit and the less damage is done */
	    modifier = chit.carried->range_attack - 
		      (player_target->defense + 3*dist/4);
	    damage = chit.carried->range_attack - dist/2;
	  }
	roll = dice(2) + modifier;
	if (debug) printf("target's hits are %d",player_target->hits);
	if (roll < 8) return -2;                /* need 8+ to hit */
	else if (roll == 8) dam_add = -3;
	else if (roll < 10) dam_add = -2;       /* the better the roll, */
	else if (roll < 12) dam_add = -1;       /* the better the damage */
	else dam_add = 0;
	if (debug) printf("roll = %d",roll);
	if ((damage + dam_add) > 0)
	  {
	    player_target->hits -= (damage + dam_add);  /* apply damage */
	    if (debug) printf("target's hits are %d",player_target->hits);
	    if (player_target->hits <= 0)       /* character dead! (sob) */
	      {
		sprintf(msg,"%s is dead!\007 (hit key)",
		  player_target->c_name);
		/* drop whatever the character was carrying */
		mvaddch(curx,cury,player_target->carried->image);
		if (player_target->image == 'D')
		  {     /* Bart & Prof are overcome... reduce some scores */
		    pp->hand_attack--;
		    pp->movement--;
		    ph->hand_attack -= 2;
		    ph->movement--;
		  }
		if (debug) printf("character is dead! ");
	      }
	    else if (player_target->hits < 2)
	      sprintf(msg,"%s is badly wounded! (hit key)",
		player_target->c_name);
	    else if (((player_target->hits == 2) && (target == 'P')) ||
		 ((player_target->hits == 3) && (target == 'D')) ||
		 ((player_target->hits == 4) && (target == 'H')))
		  sprintf(msg,"%s is unhurt (hit key)",
		    player_target->c_name);
	    else if ((player_target->hits == 2) || ((player_target->hits == 3)
					       && (target == 'H')))
		  sprintf(msg,"%s is injured! (hit key)",
		    player_target->c_name);
	  }
	else sprintf(msg,"Glancing blow - no damage (hit key)");
	tell(msg, 1);
	return 1;
      }
    else return 0;      /* it's an item of equipment & won't affect attacks */
  }

int gen_attack(chit,pp,pd,ph,pc,robot,mutant,min_dist,max_dist,direction,mode)
  struct piece chit;
  struct piece *pp,*pd,*ph,*pc,robot[num_robots],mutant[num_mutants];
  int min_dist;                 /* how far away defender must be */
  int max_dist;                 /* how far away the defender can be */
  char direction;               /* the direction the defender stands in */
  int mode;                     /* whether it's h-t-h (0) or range (1) */

  /* generic attack function, either hth or ranged, to limit of distance */

  {
    int i,j;
    int curx, cury;
    char target;
    int result, at_done;
    char msg[60];
    int nodec;

    if (debug3) 
      {
	sprintf(msg,"in gen_attack, max_dist = %d",max_dist);
	tell(msg,1);
      }
    curx = chit.xloc;
    cury = chit.yloc;
    i = 1; at_done = 0;                 /* set 'done' flag to false */
    while ((i<=max_dist) && (!at_done)) /* check to extent of range */
      {                                 /* and whether attack has been */
	nodec = 0;
	if (debug3)
	  {
	    sprintf(msg,"i = %d in i<=max_dist",i);
	    tell(msg,1);
	  }
	switch(direction)               /* made already */
	  {
	    case 'h': case '4':
	      target =  mvinch(curx,--cury);
	      break;
	    case 'l': case '6':
	      target =  mvinch(curx,++cury);
	      break;
	    case 'j': case '2':
	      target =  mvinch(++curx,cury);
	      break;
	    case 'k': case '8':
	      target =  mvinch(--curx,cury);
	      break;
	    case 'u': case '-': case '0':       /* cancel attack */
	      return 0;
	      break;
	    case 'r': fixscreen();              /* no break! */
	    default:
	      sprintf(msg,"hit h(4), j(2), k(8), or l(6) for directions");
	      tell(msg, 0);
	      direction = getch();
	      nodec = 1;
	      wclear(messes);
	      wrefresh(messes);
	  }
	  /* if it's blank space or equipment, skip it */
	if (debug) printf("target is %c",target);
	if ((!nodec) && (!(result = resolve(chit,pp,pd,ph,pc,robot,
	  mutant,mode,target,curx,cury,min_dist,i)))) i++;
	else            /* return value from resolve != 0 */
	  {
	    if (debug3)
	      {
		sprintf(msg,"i=%d, result=%d (should be != 0)",i,result);
		tell(msg,1);
	      }
	    if (result == -3)
	      sprintf(msg,"Target too close for ranged attack (hit key)");
	    else if (result == -2)
	      sprintf(msg,"%s missed on the attack (hit key)",
		  chit.c_name);
	    else if (result == -1)
	      sprintf(msg,"%s hit the wall (hit key)",
		  chit.c_name);
	    if (debug) printf("result = %d",result);
	    if ((result != 1) && (!nodec)) tell(msg, 1);
	    if (((chit.carried->image != '}') ||
		(target == '#')) && (!nodec)) at_done = 1;
	  }
      }
    if (i > max_dist)
      {
	sprintf(msg,"Nothing (else) in range. (hit key)");
	tell(msg, 1);
      }
    return 1;
  }

mutie_attack(pp,pd,ph,pc,robot,mutant)
  struct piece *pp, *pd, *ph, *pc, robot[num_robots], mutant[num_mutants];

  {
    int i;
    char hdir, jdir, kdir, ldir;
    char msg[60];

    for (i = 0; i < num_mutants; i++)
      {
	if (mutant[i].hits > 0)                 /* skip dead mutants */
	  {
	    if (debug3)
	      {
		sprintf(msg,"Mutant %d's hits: %d",i,mutant[i].hits);
		tell(msg,1);
	      }
		/* don't even check things off-screen */
	    if (mutant[i].yloc > 7)
	      hdir = mvinch(mutant[i].xloc, mutant[i].yloc-1);
	    else hdir = ' ';
	    if (mutant[i].xloc < 19)
	      jdir = mvinch(mutant[i].xloc+1, mutant[i].yloc);
	    else jdir = ' ';
	    if (mutant[i].xloc > 0)
	      kdir = mvinch(mutant[i].xloc-1, mutant[i].yloc);
	    else kdir = ' ';
	    if (mutant[i].yloc < 59)
	      ldir = mvinch(mutant[i].xloc, mutant[i].yloc+1);
	    else ldir = ' ';
	    if (debug3)
	      {
		sprintf(msg,"Mutant %d checking for attack ",i);
		tell(msg,1);
		sprintf(msg,"h=%c, j=%c, k=%c, l=%c",hdir,jdir,kdir,ldir);
		tell(msg,1);
	      }
		/* go after the humans first */
	    if ((hdir == 'P') || (hdir == 'D') || (hdir == 'H'))
	      gen_attack(mutant[i],pp,pd,ph,pc,robot,mutant,1,1,'h',0);
	    else if ((jdir == 'P') || (jdir == 'D') || (jdir == 'H'))
	      gen_attack(mutant[i],pp,pd,ph,pc,robot,mutant,1,1,'j',0);
	    else if ((kdir == 'P') || (kdir == 'D') || (kdir == 'H'))
	      gen_attack(mutant[i],pp,pd,ph,pc,robot,mutant,1,1,'k',0);
	    else if ((ldir == 'P') || (ldir == 'D') || (ldir == 'H'))
	      gen_attack(mutant[i],pp,pd,ph,pc,robot,mutant,1,1,'l',0);
		/* then go after the robots & computer */
	    else if ((hdir == 'R') || (hdir == 'C'))
	      gen_attack(mutant[i],pp,pd,ph,pc,robot,mutant,1,1,'h',0);
	    else if ((jdir == 'R') || (jdir == 'C'))
	      gen_attack(mutant[i],pp,pd,ph,pc,robot,mutant,1,1,'j',0);
	    else if ((kdir == 'R') || (kdir == 'C'))
	      gen_attack(mutant[i],pp,pd,ph,pc,robot,mutant,1,1,'k',0);
	    else if ((ldir == 'R') || (ldir == 'C'))
	      gen_attack(mutant[i],pp,pd,ph,pc,robot,mutant,1,1,'l',0);
	    else if (debug3)
	      {
		sprintf(msg,"Mutant %d has nothing to attack",i);
		tell(msg,1);
	      }
	  }
      }
  }

int target(chit,dist)
  struct piece chit;
  int dist;

  {
    int hdir,jdir,kdir,ldir,i,cksq;
    char spot;

    i = hdir = jdir = kdir = ldir = 1;
    while (i <= dist)
      {
	if (hdir)
	  {
	    spot = mvinch(chit.xloc, chit.yloc - i);
	    if ((spot == '+') || (spot == '#') || 
		((chit.yloc - i) < 7)) hdir = 0;
	    else if (!checksquare(spot)) return 1;
	  }
	if (jdir)
	  {
	    spot = mvinch(chit.xloc + i, chit.yloc);
	    if ((spot == '+') || (spot == '#') || 
		((chit.xloc + i) > 19)) jdir = 0;
	    else if (!checksquare(spot)) return 1;
	  }
	if (kdir)
	  {
	    spot = mvinch(chit.xloc - i, chit.yloc);
	    if ((spot == '+') || (spot == '#') || 
		((chit.xloc - i) < 0)) kdir = 0;
	    else if (!checksquare(spot)) return 1;
	  }
	if (ldir)
	  {
	    spot = mvinch(chit.xloc, chit.yloc + i);
	    if ((spot == '+') || (spot == '#') || 
		((chit.yloc + i) > 59)) ldir = 0;
	    else if (!checksquare(spot)) return 1;
	  }
	i++;
      }
    return 0;
  }

int hth_attack(chit,pp,pd,ph,pc,robot,mutant)
  struct piece chit;
  struct piece *pp, *pd, *ph, *pc, robot[num_robots], mutant[num_mutants];

  {
    char compl_mess[60];
    static char dirmsg[] = "Which direction? ";
    char decision;
    char direction;
    int min_dist, max_dist, mode;

    if ((!chit.hand_attack) || (!target(chit,1))) return 0;
    min_dist = max_dist = 1; mode = 0;
    sprintf(compl_mess,"Hand attack with %s (STR %d)? (n or 0 for no)",
	    chit.c_name, chit.hand_attack + chit.carried->attack_add);
    move(chit.xloc, chit.yloc);
    tell(compl_mess, 0);                        /* ask 'em if they wanna */
    decision = getch();
    if ((decision == 'n') || (decision == '0'))  /* nope - return 'em and */
	return 0;                               /* ask if they want range */
    tell(dirmsg, 0);                            /* ask for direction of att */
    direction = getch();
    if (debug) printf("going from hth to general attack");
    if (!(gen_attack
	 (chit,pp,pd,ph,pc,robot,mutant,min_dist,max_dist,direction,mode)))
	return 0;
    if (debug) printf("out of general attack");
    return 1;
  }

range_attack(chit,pp,pd,ph,pc,robot,mutant)
  struct piece chit;
  struct piece *pp, *pd, *ph, *pc, robot[num_robots], mutant[num_mutants];

  {
    int i, mode = 1, min_dist;
    char decision, direction;
    char compl_mess[60];
    static char dirmsg[] = "Which direction? ";

    if ((!chit.carried->range_attack) || 
	(!target(chit,chit.carried->distance))) return;
    /* a rifle or the secret weapon may not attack adjacent squares */
    if ((chit.carried->image == '>') || (chit.carried->image == '}'))
      min_dist = 2;
    else min_dist = 1;
    sprintf(compl_mess,"Range attack with %s (STR %d)? (n or 0 for no)",
	    chit.c_name, chit.carried->range_attack);
    move(chit.xloc, chit.yloc);
    tell(compl_mess, 0);                        /* ask 'em if they wanna */
    decision = getch();
    if ((decision == 'n') || (decision == '0')) return; /* nope - return 'em */
    if (decision == 'r') fixscreen();
    tell(dirmsg, 0);                            /* ask for direction of att */
    direction = getch();
    gen_attack(chit,pp,pd,ph,pc,robot,mutant,min_dist,
		chit.carried->distance,direction,mode);
  }

player_combat(pp, pd, ph, pc, robot, mutant)
  struct piece *pp, *pd, *ph, *pc, robot[num_robots], mutant[num_mutants];

  {
    int i;

    if (pp->hits > 0)                   /* if prof is still alive */
      if (!hth_attack(*pp,pp,pd,ph,pc,robot,mutant)) 
	range_attack(*pp,pp,pd,ph,pc,robot,mutant);
    if (pd->hits > 0)                   /* daughter Molly */
      if (!hth_attack(*pd,pp,pd,ph,pc,robot,mutant)) 
	range_attack(*pd,pp,pd,ph,pc,robot,mutant);
    if (ph->hits > 0)                   /* hero Bart */
      if (!hth_attack(*ph,pp,pd,ph,pc,robot,mutant)) 
	range_attack(*ph,pp,pd,ph,pc,robot,mutant);
	/* if main computer is dead, robots can't range attack */
    for (i = 0; i < num_robots; i++)
      if (robot[i].hits > 0)
	if ((!hth_attack(robot[i],pp,pd,ph,pc,robot,mutant)) 
	  && (pc->hits > 0)) range_attack(robot[i],pp,pd,ph,pc,robot,mutant);
  }

/* Movement Section */


char pickup(chit, number)               /* pick up what's in the square */
  struct piece *chit;           /* lose what is already carried */
  int number;

  {
    char msg[60], drop;

    if (debug2) printf("in pickup");
    drop = chit->carried->image;
    chit->carried = list+number;
    sprintf(msg,"%s has picked up a %s (hit key)",
		chit->c_name,list[number].item);
    tell(msg, 1);                         /* inform player of pick-up */
    return(drop);
  }

identify(quest)
  char quest;

  {
    int csq;
    char msg[60];

	/* check if it's equipment */
    if ((csq = checksquare(quest)) > 0)
      {
	sprintf(msg,"'%c' = %s (hit key)",quest,list[csq].item);
	tell(msg,1);
      }
    else
      {
	switch (quest)
	  {
	    case 'M': sprintf(msg,"Evil Mutant (hit key)");
		      break;
	    case 'S': sprintf(msg,"Evil Super Mutant (hit key)");
		      break;
	    case 'Z': sprintf(msg,"Evil Mutant Zombie (hit key)");
		      break;
	    case 'R': sprintf(msg,"Cute Robot (hit key)");
		      break;
	    case 'C': sprintf(msg,"Main Control Computer (hit key)");
		      break;
	    case 'P': sprintf(msg,"Absent-minded Professor (hit key)");
		      break;
	    case 'D': sprintf(msg,"Prof's daughter, Molly (hit key)");
		      break;
	    case 'H': sprintf(msg,"Dumb hero, Bart (hit key)");
		      break;
	    case '#': sprintf(msg,"A wall (hit key)");
		      break;
	    case ' ': sprintf(msg,"Open key (hit key)");
		      break;
	    case '+': sprintf(msg,"A door (hit key)");
		      break;
	    case 'q': case 'Q': sprintf(msg,"Quit game");
				break;
	    case 'h': case '4': sprintf(msg,"Left (hit key)");
			      break;
	    case 'j': case '2': sprintf(msg,"Down (hit key)");
			      break;
	    case 'k': case '8': sprintf(msg,"Up (hit key)");
			      break;
	    case 'l': case '6': sprintf(msg,"Right (hit key)");
			      break;
	    case 's': case '3': sprintf(msg,"Stop (hit key)");
			      break;
	    case 'w': case '1': sprintf(msg,"Work on Secret Weapon (hit key)");
			      break;
	    case 'd': case '9': sprintf(msg,"Drop carried (hit key)");
			      break;
	    case 'm': case '5': sprintf(msg,
				"Move without pickup (hit key)");
			      break;
	    case 'i': case '7': sprintf(msg,"Inventory (hit key)");
			      break;
	    case '/': case ',': sprintf(msg,"Show Keypad (hit key)");
			      break;
	    case '0': case 'n': 
			      sprintf(msg,"Skip move or attack (hit key)");
			      break;
	    case '?': sprintf(msg,"Identify a key (hit key)");
			      break;
	    case '-': sprintf(msg,"Identify a key (or undo attack) (hit key)");
			      break;
	    case 'u': sprintf(msg,
		"Undo attack (i.e. opt for other attack) (hit key)");
			      break;
	    case '.': case 'f': sprintf(msg,"Build a robot");
			      break;
	    default: sprintf(msg,"Key %c not known (hit key)",quest);
		     break;
	  }
	tell(msg,1);
      }
  }

keypad()

  {
    FILE *kypd;
    WINDOW *keys;
    char msg[60];
    int i;

    if ((kypd = fopen("mutants.key","r")) == NULL)
      {
	sprintf(msg,"Keypad file not found (hit key)");
	tell(msg,1);
	return;
      }
    keys = newwin(20,66,0,0);
    for (i = 0; i < 19; i++)
      {
	fgets(msg,66,kypd);
	mvwaddstr(keys,i,4,msg);
      }
    fclose(kypd);
    sprintf(msg,"Hit key to continue");
    tell(msg,0);
    wgetch(keys);
    delwin(keys);
  }

int any_parts(prof,hsq,jsq,ksq,lsq)             /* any spare parts nearby? */
  struct piece *prof;
  int *hsq, *jsq, *ksq, *lsq;

  {
    *hsq = mvinch(prof->xloc, prof->yloc-1);
    *jsq = mvinch(prof->xloc+1, prof->yloc);
    *ksq = mvinch(prof->xloc-1, prof->yloc);
    *lsq = mvinch(prof->xloc, prof->yloc+1);
    if ((prof->carried->image != '$') && (*hsq != '$') && (*jsq != '$') &&
	(*ksq != '$') && (*lsq != '$')) return 0;
    else return 1;
  }

repair(robot, prof, which)
  struct piece robot[num_robots],*prof;
  int which;

  {
    char msg[60];
    char where;
    int hsq,jsq,ksq,lsq;
    int dropped, toomany;
    int poss;
  
    dropped = toomany = 0;
    if (!any_parts(prof, &hsq, &jsq, &ksq, &lsq))
      {
	sprintf(msg,"Prof needs spare parts (next to or carried) (hit key)");
	tell(msg,1);
	return;
      }
    /* slide rule helps a little in repairs */
    if (prof->carried->image == ':') poss = 3;
    else poss = 4;
    if (!(rndm() % poss))
      {
	sprintf(msg,"Success!  Prof has made a Robot (hit key)");
	tell(msg,1);
	/* take away spare parts, if they're still around */
	if (hsq == '$') 
	  {
	    robot[which].xloc = prof->xloc;
	    robot[which].yloc = prof->yloc - 1;
	  }
	else if (jsq == '$') 
	  {
	    robot[which].xloc = prof->xloc + 1;
	    robot[which].yloc = prof->yloc;
	  }
	else if (ksq == '$') 
	  {
	    robot[which].xloc = prof->xloc - 1;
	    robot[which].yloc = prof->yloc;
	  }
	else if (lsq == '$') 
	  {
	    robot[which].xloc = prof->xloc;
	    robot[which].yloc = prof->yloc + 1;
	  }
	else while ((!dropped) && (toomany < 10))
	  {
	    toomany++;
	    sprintf(msg,"Put Robot in which direction? ");
	    tell(msg,0);
	    where = getch();
	    switch (where)
	      {
		case 'h': case '4':
		  if (hsq != ' ') 
		    {
		      sprintf(msg,"Can't put there (hit key)");
		      tell(msg,1);
		      break;
		    }
		  else
		    {
		      robot[which].xloc = prof->xloc;
		      robot[which].yloc = prof->yloc - 1;
		      dropped = 1;
		    }
		  break;
		case 'j': case '2':
		  if (jsq != ' ')
		    {
		      sprintf(msg,"Can't put there (hit key)");
		      tell(msg,1);
		      break;
		    }
		  else
		    {
		      robot[which].xloc = prof->xloc + 1;
		      robot[which].yloc = prof->yloc;
		      dropped = 1;
		    }
		  break;
		case 'k': case '8':
		  if (ksq != ' ')
		    {
		      sprintf(msg,"Can't put there (hit key)");
		      tell(msg,1);
		      break;
		    }
		  else
		    {
		      robot[which].xloc = prof->xloc - 1;
		      robot[which].yloc = prof->yloc;
		      dropped = 1;
		    }
		  break;
		case 'l': case '6':
		  if (lsq != ' ')
		    {
		      sprintf(msg,"Can't put there (hit key)");
		      tell(msg,1);
		      break;
		    }
		  else
		    {
		      robot[which].xloc = prof->xloc;
		      robot[which].yloc = prof->yloc + 1;
		      dropped = 1;
		    }
		  break;
		default: 
		  sprintf(msg,
		    "h(4)=left,j(2)=down,k(8)=up,l(6)=right (hit key)");
		  tell(msg,1);
		  break;
	      }
	  }
	if (toomany == 10)
	  {
	    sprintf(msg,"Forget it - no robot for you (hit key)");
	    tell(msg,1);
	  }
	else 
	  {
	    setattr(_BOLD);
	    mvaddch(robot[which].xloc,robot[which].yloc,robot[which].image);
	    clrattr(_BOLD);
	  }
	robot[which].carried = Nothing_l;
	robot[which].hits = 2;
	refresh();
      }
    else 
      {
	sprintf(msg,"Prof failed to make a robot (hit key)");
	tell(msg,1);
	seed++;                         /* a randomizer kludge... oh well */
      }
  }

secret(pp)                      /* the prof's secret weapon */
  struct piece *pp;

  {
    int fail, chance, sal_add, hsq, jsq, ksq, lsq;
    char msg[60];

    /* professor must have spare parts carried or next to him */
    if (!any_parts(pp, &hsq, &jsq, &ksq, &lsq))
      {
	sprintf(msg,"Prof needs spare parts (next to or carried) (hit key)");
	tell(msg,1);
	return;
      }
    /* determine if prof is being crowded by mutants */
    if ((hsq == 'M') || (hsq == 'S') || (jsq == 'M') || (jsq == 'S') ||
	(lsq == 'M') || (lsq == 'S') || (ksq == 'M') || (ksq == 'S') ||
	(hsq == 'Z') || (jsq == 'Z') || (ksq == 'Z') || (lsq == 'Z'))
      {
	sprintf(msg,"Can't concentrate - Mutant too close (hit key)");
	tell(msg,1);
	return;
      }
    /* computer and slide rule (ha!) can aid in calculations */
    if ((hsq == 'C') || (jsq == 'C') || (ksq == 'C') || (lsq == 'C'))
      sal_add = 3;
    else
      {
	sal_add = 0;
	sprintf(msg,"Perhaps BERT could help... (hit key)");
	tell(msg,1);
      }
    if (pp->carried->image == ':') chance = 7 - sal_add;
    else
      {
	chance = 10 - sal_add;
	sprintf(msg,"The prof could use his slide rule (hit key)");
	tell(msg,1);
      }
    fail = rndm() % chance;
    if (fail)
      {
	sprintf(msg,"Sorry, the prof blew it (hit key)");
	tell(msg,1);
      }
    else
      {
	sprintf(msg,"Success!  Prof now has Weapon (hit key)");
	tell(msg,1);
	/* take away spare parts, if they're still around */
	if (hsq == '$') mvaddch(pp->xloc,pp->yloc-1,pp->carried->image);
	else if (jsq == '$') mvaddch(pp->xloc+1,pp->yloc,pp->carried->image);
	else if (ksq == '$') mvaddch(pp->xloc-1,pp->yloc,pp->carried->image);
	else if (lsq == '$') mvaddch(pp->xloc,pp->yloc+1,pp->carried->image);
	pp->carried = Secret_Weapon_l;
      }
  }

char look(looker, lastmove)             /* how mutants see targets */
  struct piece looker;
  int lastmove;                         /* where this mutant last moved */

  {
    int i, found, ldir, hdir, jdir, kdir, ifdoor, ifequip;
    char target, slong, hone, jone, kone, lone;
    char msg[60];

	/* found is the key to which direction to go: */
	/* 1=>'h' (left), 2=>'j' (down), 3=>'k' (up), 4=>'l' (right) */

    slong = '0';
    ldir = hdir = jdir = kdir = 1;
    ifdoor = ifequip = found = i = 0;
    while ((i++ < 21) && (!found))      /* until found or at end of sight */
      {
	if (hdir)
	  {
	    target = mvinch(looker.xloc, looker.yloc - i);
	    /* if we're off the screen or hit a wall, stop searching */
	    if (((looker.yloc - i) < 7) || (target == '#')
	       || (((target == 'M') || (target == 'S') || (target == 'Z'))
	       && (i == 1))) hdir = 0;
	    else if ((target != ' ') && (target != 'M') 
		  && (target != 'S') && (target != 'Z'))
	      {
		/* if it's equipment, remember it as a possible target */
		if ((checksquare(target)) > 0)
		  {
		    if ((!ifequip) && (looker.carried->image == ' ')) 
		      ifequip = 1;
		  }
		/* if it's not a door, it must be something to eat */
		else if (target != '+')
		  {
		    found = 1;          /* key for direction 'h' */
		    break;
		  }
		/* if it's a door, remember it as a possible target. */
		else if (!ifdoor) ifdoor = 1;
		if (debug3)
		  {
		    sprintf(msg,"tar=%c, dor=%d, fnd=%d, qip=%d, im='%c'",
			target,ifdoor,found,ifequip,looker.carried->image);
		    tell(msg, 1);
		  }
	      }
	    else if ((target == ' ') && (lastmove != 'l') 
		     && (slong == '0')) slong = 'h';
	  }
	if (jdir)
	  {
	    target = mvinch(looker.xloc + i, looker.yloc);
	    /* if we're off the screen or hit a wall, stop searching */
	    if (((looker.xloc + i) > 19) || (target == '#')
	       || (((target == 'M') || (target == 'S') || (target == 'Z'))
	       &&  (i == 1))) jdir = 0;
	    else if ((target != ' ') && (target != 'M') 
		  && (target != 'S') && (target != 'Z'))
	      {
		/* if it's equipment, remember it as a possible target */
		if ((checksquare(target)) > 0)
		  {
		    if ((!ifequip) && (looker.carried->image == ' ')) 
		      ifequip = 2;
		  }
		/* if it's not a door, it must be something to eat */
		else if (target != '+')
		  {
		    found = 2;          /* key for direction 'j' */
		    break;
		  }
		/* if it's a door, remember it as a possible target. */
		else if (!ifdoor) ifdoor = 2;
		if (debug3)
		  {
		    sprintf(msg,"tar=%c, dor=%d, fnd=%d, qip=%d, im='%c'",
			target,ifdoor,found,ifequip,looker.carried->image);
		    tell(msg, 1);
		  }           }
	    else if ((target == ' ') && (lastmove != 'k')
		     && (slong == '0')) slong = 'j';
	  }
	if (kdir)
	  {
	    target = mvinch(looker.xloc - i, looker.yloc);
	    /* if we're off the screen or hit a wall, stop searching */
	    if (((looker.xloc - i) < 0) || (target == '#')
	       || (((target == 'M') || (target == 'S') || (target == 'Z')) 
	       &&  (i == 1))) kdir = 0;
	    else if ((target != ' ') && (target != 'M') && (target != 'S'))
	      {
		/* if it's equipment, remember it as a possible target */
		if ((checksquare(target)) > 0)
		  {
		    if ((!ifequip) && (looker.carried->image == ' ')) 
		      ifequip = 3;
		  }
		/* if it's not a door, it must be something to eat */
		else if (target != '+')
		    {
		      found = 3;                /* key for direction 'k' */
		      break;
		    }
		/* if it's a door, remember it as a possible target. */
		else if (!ifdoor) ifdoor = 3;
		if (debug3)
		  {
		    sprintf(msg,"tar=%c, dor=%d, fnd=%d, qip=%d, im='%c'",
			target,ifdoor,found,ifequip,looker.carried->image);
		    tell(msg, 1);
		  }           }
	    else if ((target == ' ') && (lastmove != 'j')
		    && (slong == '0')) slong = 'k';
	  }
	if (ldir)
	  {
	    target = mvinch(looker.xloc, looker.yloc + i);
	    /* if we're off the screen or hit a wall, stop searching */
	    if (((looker.yloc + i) > 59) || (target == '#')
	       || (((target == 'M') || (target == 'S') || (target == 'Z')) 
	       &&  (i == 1))) ldir = 0;
	    else if ((target != ' ') && (target != 'M') && (target != 'S'))
	      {
		/* if it's equipment, remember it as a possible target */
		if ((checksquare(target)) > 0)
		  {
		    if ((!ifequip) && (looker.carried->image == ' ')) 
		      ifequip = 4;
		  }
		/* if it's not a door, it must be something to eat */
		else if (target != '+')
		  {
		    found = 4;          /* key for direction 'h' */
		    break;
		  }
		/* if it's a door, remember it as a possible target. */
		else if (!ifdoor) ifdoor = 4;
		if (debug3)
		  {
		    sprintf(msg,"tar=%c, dor=%d, fnd=%d, qip=%d, im='%c'",
			target,ifdoor,found,ifequip,looker.carried->image);
		    tell(msg, 1);
		  }
	      }
	    else if ((target == ' ') && (lastmove != 'l')
		    && (slong == '0')) slong = 'l';
	  }
      }
    if (!found)
      {
	if (debug3) 
	  {
	    sprintf(msg,"slong = %c, ifdoor = %d",slong,ifdoor);
	    tell(msg,1);
	  }
	/* if there's equipment around & you need it, go for it */
	switch (ifequip)
	  {
	    case 1: return 'h';
		    break;
	    case 2: return 'j';
		    break;
	    case 3: return 'k';
		    break;
	    case 4: return 'l';
		    break;
	    default: break;
	  }
	/* a door is almost as good as a target */
	switch (ifdoor)
	  {
	    case 1: if (lastmove != 'l') return 'h';
		break;
	    case 2: if (lastmove != 'k') return 'j';
		break;
	    case 3: if (lastmove != 'j') return 'k';
		break;
	    case 4: if (lastmove != 'h') return 'l';
		break;
	    default: break;
	  }
	/* if slong hasn't been assigned, give it some simple value */
	if (slong == '0') switch (lastmove)
	  {
	    case 'j': if (looker.xloc != 0) slong = 'k';
		    break;
	    case 'k': if (looker.xloc != 19) slong = 'j';
		    break;
	    case 'l': if (looker.yloc != 7) slong = 'h';
		    break;
	    case 'h': if (looker.yloc != 59) slong = 'l';
		    break;
	  }
		/* need to keep the mutants from bumping into walls and */
		/* edges of screen repeatedly.  */
	    /* all possible edges & lastmoves, in one statement */
	if (((looker.xloc == 0) && (lastmove == 'k'))
	 || ((looker.xloc == 19) && (lastmove == 'j'))
	 || ((looker.yloc == 7) && (lastmove == 'h'))
	 || ((looker.yloc == 59) && (lastmove == 'l')))
	   return slong;
	    /* any direction, with a wall in the wrong spot */
	kone = mvinch(looker.xloc-1,looker.yloc);
	jone = mvinch(looker.xloc+1,looker.yloc);
	hone = mvinch(looker.xloc,looker.yloc-1);
	lone = mvinch(looker.xloc,looker.yloc+1);
	if (((lastmove == 'k') && ((kone == 'M') ||
	     (kone == 'S') || (kone == 'Z') || (kone == '#')))
	 || ((lastmove == 'j') && ((jone == 'M') ||
	     (jone == 'S') || (kone == 'Z') || (jone == '#')))
	 || ((lastmove == 'h') && ((hone == 'M') ||
	     (hone == 'S') || (kone == 'Z') || (hone == '#')))
	 || ((lastmove == 'l') && ((lone == 'M') ||
	     (lone == 'S') || (kone == 'Z') || (lone == '#'))))
	  return slong;
	return lastmove;
      }
    else switch(found)
      {
	case 1: return 'h';
	case 2: return 'j';
	case 3: return 'k';
	case 4: return 'l';
      }
  }

mutie_move(mutant, lastmove)
  struct piece mutant[num_mutants];
  char lastmove[num_mutants];

  {
    int i, which, j;
    char direction, onekey, drop;
    char msg[60];

    for (i = 0; i < num_mutants; i++)
      {
	if (mutant[i].hits > 0)
	  {
	    if (debug3)
	      {
		move(mutant[i].xloc,mutant[i].yloc);
		sprintf(msg,"Mutant %d, %d hits, moving ",i,mutant[i].hits);
		tell(msg,1);
	      }
	    for (j = 0; j < mutant[i].movement; j++)
	      {
		direction = look(mutant[i],lastmove[i]);
		switch (direction)
		  {
		    case 'h':
		      onekey = mvinch(mutant[i].xloc,mutant[i].yloc-1);
		      if (which = checksquare(onekey))
			{
			  /* pick up equipment, if it's there */
			  if (which > 0) 
			    {
			      drop = pickup(mutant+i,which);
			      /* drop what you're carrying */
			      mvaddch(mutant[i].xloc,mutant[i].yloc,drop);
			    }
			  else mvaddch(mutant[i].xloc,mutant[i].yloc,' ');
			  mutant[i].yloc--;
			  setattr(_BOLD);
			  mvaddch(mutant[i].xloc,mutant[i].yloc,
				mutant[i].image);
			  clrattr(_BOLD);
			  lastmove[i] = 'h';
			}     
		      break;
		    case 'j':
		      onekey = mvinch(mutant[i].xloc+1,mutant[i].yloc);
		      if (which = checksquare(onekey))
			{
			  /* pick up equipment, if it's there */
			  if (which > 0) 
			    {
			      drop = pickup(mutant+i,which);
			      /* drop what you're carrying */
			      mvaddch(mutant[i].xloc,mutant[i].yloc,drop);
			    }
			  else mvaddch(mutant[i].xloc,mutant[i].yloc,' ');
			  mutant[i].xloc++;
			  setattr(_BOLD);
			  mvaddch(mutant[i].xloc,mutant[i].yloc,mutant[i].image)
;
			  clrattr(_BOLD);
			  lastmove[i] = 'j';
			}     
		      break;
		    case 'k':
		      onekey = mvinch(mutant[i].xloc-1,mutant[i].yloc);
		      if (which = checksquare(onekey))
			{
			  /* pick up equipment, if it's there */
			  if (which > 0) 
			    {
			      drop = pickup(mutant+i,which);
			      /* drop what you're carrying */
			      mvaddch(mutant[i].xloc,mutant[i].yloc,drop);
			    }     
			  else mvaddch(mutant[i].xloc,mutant[i].yloc,' ');
			  mutant[i].xloc--;
			  setattr(_BOLD);
			  mvaddch(mutant[i].xloc,mutant[i].yloc,mutant[i].image);
			  clrattr(_BOLD);
			  lastmove[i] = 'k';
			}
		      break;
		    case 'l':
		      onekey = mvinch(mutant[i].xloc,mutant[i].yloc+1);
		      if (which = checksquare(onekey))
			{
			  /* pick up equipment, if it's there */
			  if (which > 0) 
			    {
			      drop = pickup(mutant+i,which);
			      /* drop what you're carrying */
			      mvaddch(mutant[i].xloc,mutant[i].yloc,drop);
			    }
			  else mvaddch(mutant[i].xloc,mutant[i].yloc,' ');
			  mutant[i].yloc++;
			  setattr(_BOLD);
			  mvaddch(mutant[i].xloc,mutant[i].yloc,mutant[i].image)
;
			  clrattr(_BOLD);
			  lastmove[i] = 'l';
			}     
		      break;
		  }
		if (j >= 2) refresh();
	      }
	  }
      }
    refresh();
  }

resurrect(mutant,howmany)
  struct piece mutant[num_mutants];
  int howmany;

  {
    int i,j;
    char msg[60], mcheck;

    for (i = 0; i < howmany; i++)
      {
	j = rndm() % num_mutants;
	mcheck = mvinch(mutant[j].xloc,mutant[j].yloc);
	if ((mutant[j].hits < 0) && (mcheck == ' '))
	  {
	    /* the mutant is dead => resurrect it */
	    strcpy(mutant[j].c_name,"Mutant Zombie");
	    mutant[j].image = 'Z';
	    mutant[j].hits = 3;
	    mutant[j].movement = 3;
	    mutant[j].carried = Nothing_l;
	    sprintf(msg,"Mutant rises from the dead! (hit key)");
	    setattr(_BOLD);
	    mvaddch(mutant[j].xloc,mutant[j].yloc,mutant[j].image);
	    clrattr(_BOLD);
	    tell(msg,1);
	  }
	else seed++;            /* make sure we aren't looping */
      }
  }

movman(chit,wave,robot)                 /* moving the player's pieces */
  struct piece *chit;
  int wave;
  struct piece robot[num_robots];

  {
    char direction, c, msg[60], drop;
    int i, total_moves, mvck;
    char ddir, dchk, nextsquare;
    int dx,dy;
    int mcheck, ycoord, xcoord;

    if (debug) printf("about to set up move message");
    if (debug) printf("here's chit->c_name! %s",chit->c_name);
	/* advise player of movement value of piece */
    total_moves = 0;            /* keep track of how far they've moved */
    do
      {
	sprintf(msg,"%s, Movement = %d",
		chit->c_name, chit->movement-total_moves);
	tell(msg, 0);
	refresh();
	setattr(_BOLD);
	mvaddch(chit->xloc,chit->yloc,chit->image);
	clrattr(_BOLD);
	move(chit->xloc, chit->yloc);   /* put cursor in right place */
	direction = getch();    /* see which way they want to go: */
	switch(direction)
	  {
	    case 'k': case '8':         /* up */
	      move(chit->xloc-1,chit->yloc);
	      if (!(mvck = checksquare(inch()))) break;
	      if (chit->xloc == 0) break;
	      if (mvck != -1) 
		{
		  drop = pickup(chit,mvck);
		  mvaddch(chit->xloc,chit->yloc,drop);
		}
	      else mvaddch(chit->xloc,chit->yloc,' ');
	      (chit->xloc)--;
	      break;
	    case 'h': case '4':         /* left */
	      move(chit->xloc,chit->yloc-1);
	      if (!(mvck = checksquare(inch()))) break;
	      if (chit->yloc == 7) break;
	      if (mvck != -1) 
		{
		  drop = pickup(chit,mvck);
		  mvaddch(chit->xloc,chit->yloc,drop);
		}
	      else mvaddch(chit->xloc,chit->yloc,' ');
	      (chit->yloc)--;
	      break;
	    case 'l': case '6':         /* right */
	      move(chit->xloc,chit->yloc+1);
	      if (!(mvck = checksquare(inch()))) break;
	      if (chit->yloc == 59) break;
	      if (mvck != -1) 
		{
		  drop = pickup(chit,mvck);
		  mvaddch(chit->xloc,chit->yloc,drop);
		}
	      else mvaddch(chit->xloc,chit->yloc,' ');
	      (chit->yloc)++;
	      break;
	    case 'j': case '2':         /* down */
	      move(chit->xloc+1,chit->yloc);
	      if (!(mvck = checksquare(inch()))) break;
	      if (chit->xloc == 19) break;
	      if (mvck != -1) 
		{
		  drop = pickup(chit,mvck);
		  mvaddch(chit->xloc,chit->yloc,drop);
		}
	      else mvaddch(chit->xloc,chit->yloc,' ');
	      (chit->xloc)++;
	      break;
	    case 'm': case '5':         /* move w/out pickup */
	      xcoord = chit->xloc;
	      ycoord = chit->yloc;
	      sprintf(msg,"Direction? ");
	      tell(msg,0);
	      direction = getch();
	      switch (direction)
		{
		  case 'h': case '4':
		    ycoord--;
		    break;
		  case 'j': case '2':
		    xcoord++;
		    break;
		  case 'k': case '8':
		    xcoord--;
		    break;
		  case 'l': case '6':
		    ycoord++;
		    break;
		  default: break;
		}
	      nextsquare = mvinch(xcoord, ycoord);
	      if (!(mcheck = checksquare(nextsquare)))
		{
		  sprintf(msg,"Can't move there! (hit key)");
		  tell(msg,1);
		  total_moves--;
		  break;
		}
	      else if (mcheck < 0)
		{
		  sprintf(msg,"Nothing to move through (hit key)");
		  tell(msg,1);
		  total_moves--;
		  break;
		}
	      else              /* there's actually something there */
		{
		  mvaddch(chit->xloc,chit->yloc,list[mcheck].image);
		  chit->xloc = xcoord;
		  chit->yloc = ycoord;
		  /* do we need anothing mvaddch?  don't think so */
		}
	      break;
	    case 'f': case '.':                 /* make a robot */
	      if (chit->image != 'P')
		{
		  sprintf(msg,"Only prof may make robots (hit key)");
		  tell(msg,1);
		  total_moves--;
		}
	      else if (total_moves)
		{
		  sprintf(msg,
			"Prof must spend whole turn working (hit key)");
		  tell(msg,1);
		  total_moves--;
		}
	      else 
		{
		  for (i = 0; ((i < num_robots) && (robot[i].hits > 0)); i++);
		  if (i == num_robots)
		    {
		      sprintf(msg,
			"Computer can't control that many robots (hit key)");
		      tell(msg,1);
		      total_moves--;
		      break;
		    }
		  else 
		    {
		      repair(robot,chit,i);
		      total_moves = 4;
		    }
		}
	      break;
	    case 'w': case '1':                 /* work on secret weapon */
	      if ((chit->image != 'P') || (wave != 3))
		{
		  sprintf(msg,"Only prof during 3rd wave (hit key)");
		  tell(msg,1);
		  total_moves--;
		}
	      else if (total_moves)
		{
		  sprintf(msg,
			"Prof must spend whole turn working (hit key)");
		  tell(msg,1);
		  total_moves--;
		}
	      else 
		{
		  secret(chit);
		  total_moves = 4;
		}
	      break;
	    case 'd': case '9':         /* drop what you're carrying */
	      sprintf(msg,"Drop in which direction? ");
	      tell(msg,0);
	      ddir = getch();
	      switch (ddir)
		{
		  case 'h': case '4':
		    dx = chit->xloc;  dy = chit->yloc - 1;
		    break;
		  case 'l': case '6':
		    dx = chit->xloc;  dy = chit->yloc + 1;
		    break;
		  case 'j': case '2':
		    dx = chit->xloc + 1;  dy = chit->yloc;
		    break;
		  case 'k': case '8':
		    dx = chit->xloc - 1;  dy = chit->yloc;
		    break;
		  default:
		    dx = chit->xloc; dy = chit->yloc;
		    break;
		}
	      dchk = mvinch(dx, dy);
	      if (dchk == ' ')
		{
		  mvaddch(dx, dy, chit->carried->image);
		  chit->carried = Nothing_l;
		}
	      else
		{
		  sprintf(msg,"Already something there (hit key)");
		  tell(msg,1);
		}
	      total_moves--;
	      break;
	    case 'q': case 'Q':
	      sprintf(msg,"Really quit (y/[n])? ");
	      tell(msg,0);
	      drop = getch();
	      if ((drop == 'Y') || (drop == 'y'))
		{
		  nocrmode();
		  delwin(messes);
		  endwin();
		  sprintf(msg,"set term/nonum/broad");
		  system(msg);
		  exit(0);
		}
	      else total_moves--;
	      wclear(messes);
	      break;
	    case '?': case '-':
	      sprintf(msg,"Key or character you want identified: ");
	      tell(msg,0);
	      drop = getch();
	      identify(drop);
	      total_moves--;
	      break;
	    case 'r':                           /* refresh screen */
	      total_moves--;
	      fixscreen();
	      break;
	    case '/': case ',':                 /* show the keypad */
	      keypad();
	      wclear(messes);
	      wrefresh(messes);
	      total_moves--;
	      break;
	    case 's': case '3': case '0':       /* 'stop' or 'skip' */
	      total_moves = chit->movement;
	      break;
	    case 'i': case '7':                 /* stats & inventory */
	      total_moves--;
	      sprintf(msg,
	"hth=%d, ranged=%d,dist=%d,hits=%d,carried=%s,add=%d(hit key)",
		 chit->hand_attack,chit->carried->range_attack,
		 chit->carried->distance,chit->hits,chit->carried->item,
		 chit->carried->attack_add);
	      tell(msg, 1);
	      break;
	    default:                    /* any other key */
	      total_moves--;
	      if (debug3)
		{
		  sprintf(msg,"getting %c!",direction);
		  tell(msg,1);
		}
	      sprintf(msg,
	      "h(4)=left, j(2)=down, k(8)=up, l(6)=right, s(3)=stop (hit key)");
	      tell(msg, 1);
	      break;
	  }
      }
    while (++total_moves < chit->movement);
    if (debug) printf(" outta move loop ");
    setattr(_BOLD);
    mvaddch(chit->xloc,chit->yloc,chit->image);
    clrattr(_BOLD);
    refresh();
    if (debug) printf("added final image ");
  }

dumb(chit)
  struct piece *chit;

	/* see if a character acts really stupid */
  {
    int smarts;
    char msg[60];
    int which;

    if (chit->image == 'P')
      {
	smarts = 12;            /* prof's the smartest */
	which = rndm() % 3;
	switch (which)
	  {
	    case 0: sprintf(msg,
	"Prof says: 'Can we reason with them?'\007(lose move-hit key)");
		    break;
	    case 1: sprintf(msg,
	"Prof says: 'Where's my slide rule?'\007 (lose move-hit key)");
		    break;
	    case 2: sprintf(msg,
	"Prof says: 'How peculiar.  Fascinating.'\007 (lose move-hit key)");
		    break;
	    default: break;
	  }
      }
    else if (chit->image == 'D')
      {
	smarts = 9;             /* Mol's pretty smart */
	which = rndm() % 3;
	switch (which)
	  {
	    case 0: sprintf(msg,
	"Molly screams and freezes.\007 (lose move-hit key)");
		    break;
	    case 1: sprintf(msg,
	"Molly says: 'I think I smeared my makeup.'\007(lose move-hit key)");
		    break;
	    case 2: sprintf(msg,
	"Molly breaks a heel. \007 (lose move-hit key)");
		    break;
	    default: break;
	  }
      }
    else if (chit->image == 'H')
      {
	smarts = 7;                     /* boy, is he dumb */
	which = rndm() % 4;
	switch (which)
	  {
	    case 0: sprintf(msg,
	"Bart says: 'Duhhh... what should I do?'\007 (lose move-hit key)");
		    break;
	    case 1: sprintf(msg,
	"Barts asks: 'Hey, where's Molly?'\007 (lose move-hit key)");
		    break;
	    case 2: sprintf(msg,
	"Bart says: 'I think I'm gonna grab a nap.'\007(lose move-hit key)");
		    break;
	    case 3: sprintf(msg,
	"Bart says: 'Where's the pizza I ordered?'\007(lose move-hit key)");
		    break;
	    default: break;
	  }
      }
    if (!(rndm() % smarts))
      {
	seed++;                 /* having looping problems - kludge it */
	move(chit->xloc,chit->yloc);
	tell(msg,1);
	return 1;
      }
    else return 0;
  }

redo(door)
  struct doors door[num_doors];
  /* put the doors (back) on the screen */

  {
    int i;
    char dcheck;

    for (i = 0; i < num_doors; i++)
      {
	dcheck = mvinch(door[i].xloc, door[i].yloc);
	/* if there's someone there, don't close it on them */
	if (dcheck == ' ') mvaddch(door[i].xloc,door[i].yloc,'+');
      }
    refresh();
  }

glowngo(mutant)
  struct piece mutant[num_mutants];

  {
    int i, chance;
    char msg[60];

    for (i = 0; i < num_mutants; i++)
      {
	chance = rndm() % 25;
	if ((!chance) && (mutant[i].hits > 0))
	  {
	    move(mutant[i].xloc,mutant[i].yloc);
	    mutant[i].hits = 0;
	    sprintf(msg,"%s glows radioactively and disappears (hit key)",
			mutant[i].c_name);
	    tell(msg,1);
	    mvaddch(mutant[i].xloc,mutant[i].yloc,mutant[i].carried->image);
	  }
      }
  }

main()

  {
    struct piece prof, daughter, hero, computer;
    struct piece robot[num_robots], mutant[num_mutants];
    struct piece *pp = &prof, *pd = &daughter, *ph = &hero, *pc = &computer;
    int i, j, wave, round;
    char lastmove[num_mutants];
    struct doors door[num_doors];
    int players, muties;
    char msg[60];
    int dysfun, howmany;
    char instr;

    printf("Need instructions? (y/n) ");
    scanf("%c",&instr);
    if ((instr == 'y') || (instr == 'Y'))
      {
	sprintf(msg,"type/page mutants.hlp");
	system(msg);
	printf("\t\t Hit return to continue");
	scanf("%c",&instr);
      }
    scanf("%c",&instr);
    seed = time(NULL);                  /* set up the random seed */
    initscr();                          /* curses call to set up screen */
    crmode();           /* get terminal in single-character entry mode */
    noecho();
    equipment();
    clear();
    messes = newwin(3, 65, 20, 4);      /* set up message window */
    sprintf(msg,"Broadcasts off? (y/n) ");
    tell(msg,0);
    instr = getch();
    sprintf(msg,"Setting up... ");
    tell(msg,0);
    if ((instr == 'y') || (instr == 'Y'))
      sprintf(msg,"set term/num/nobroad");
    else sprintf(msg,"set term/num/broad");
    if (!(system(msg)))
      {
	sprintf(msg,"No keypad support (hit key)");
	tell(msg,1);
      }
    drawscreen();
    assign(door);
    redo(door);
	/* Play: */
    players = 1;
    for (wave = 1; ((wave <= 3) && (players)); wave++)
      {
	setup(pp, pd, ph, pc, robot, mutant, lastmove, wave);
	round = 1;
	do
	  {
	    players = muties = 0;
	    if (!(round % 5))
	      {
		howmany = round/5;
		resurrect(mutant,howmany);
	      }
	    if (pp->hits > 0)
	      {
		if (!dumb(pp)) movman(pp,wave,robot);
		players++;
	      }
	    if (pd->hits > 0)
	      {
		if (!dumb(pd)) movman(pd,wave,robot);
		players++;
	      }
	    if (ph->hits > 0)
	      {
		if (!dumb(ph)) movman(ph,wave,robot);
		players++;
	      }
	    for (j = 0; j<num_robots; j++)
	      {
		if (robot[j].hits > 0) 
		  {
		    if (pc->hits <= 0)  /* if main computer is out, robots */
		      {                 /* may have difficulties... */
			dysfun = rndm() % 4;
			if (dysfun) movman(robot+j,wave,robot);
			else
			  {
			    sprintf(msg,
		 "Robot %d confused by lack of computer control! (hit key)");
			    tell(msg,1);
			  }
		      }
		    else movman(robot+j,wave,robot);
		  }
	      }
	    player_combat(pp,pd,ph,pc,robot,mutant);
	    wclear(messes);
	    wrefresh(messes);
	    mutie_move(mutant,lastmove);
	    mutie_attack(pp,pd,ph,pc,robot,mutant);
	    for (j = 0; j<num_mutants; j++)
	      if (mutant[j].hits > 0) muties = 1;
	    glowngo(mutant);
	    redo(door);
	    round++;
	  }
	while (players && muties);
	crmode();
	if (!muties)
	  {
	    if (wave < 3)
	      sprintf(msg,"Wave %d complete (hit key)",wave);
	    else 
	      {
		if (players == 3) 
		  sprintf(msg,"Complete Victory for Humanity! (hit key)");
		else if ((ph->hits > 0) && (pd->hits > 0))
		  sprintf(msg,"Victory for Humanity! (hit key)");
		else if (pp->hits > 0)
		  sprintf(msg,"Marginal Victory for Humanity (hit key)");
		else sprintf(msg,"Draw - Pyrrhic victory (hit key)");
	      }
	  }
	else 
	  sprintf(msg,"The Evil Mutants Triumph! (hit key)");
	tell(msg, 1);
      }
    nocrmode();
    delwin(messes);
    endwin();
    sprintf(msg,"set term/nonum/broad");
    system(msg);
  }


