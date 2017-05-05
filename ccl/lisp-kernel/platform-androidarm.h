/*
   Copyright (C) 2010 Clozure Associates
   Copyright (C) 1994-2001 Digitool, Inc
   This file is part of Clozure CL.  

   Clozure CL is licensed under the terms of the Lisp Lesser GNU Public
   License , known as the LLGPL and distributed with Clozure CL as the
   file "LICENSE".  The LLGPL consists of a preamble and the LGPL,
   which is distributed with Clozure CL as the file "LGPL".  Where these
   conflict, the preamble takes precedence.  

   Clozure CL is referenced in the preamble as the "LIBRARY."

   The LLGPL is also available online at
   http://opensource.franz.com/preamble.html
*/

#define WORD_SIZE 32
#define PLATFORM_OS PLATFORM_OS_ANDROID
#define PLATFORM_CPU PLATFORM_CPU_ARM
#define PLATFORM_WORD_SIZE PLATFORM_WORD_SIZE_32

typedef struct ucontext ExceptionInformation;

#define MAXIMUM_MAPPABLE_MEMORY ((3<<28)-(1<<16))
#define IMAGE_BASE_ADDRESS 0x50000000

#include "lisptypes.h"
#include "arm-constants.h"

/* xp accessors */
#define xpGPRvector(x) ((natural *)&((x)->uc_mcontext.arm_r0))
#define xpGPR(x,gprno) (xpGPRvector(x))[gprno]
#define xpPC(x) (*((pc*)(&(xpGPR(x,15)))))
#define xpLR(x) (*((pc*)(&(xpGPR(x,14)))))
#define xpPSR(x) xpGPR(x,16)
#define xpFaultAddress(x) xpGPR(x,17)
#define xpTRAP(x) xpGPR(x,-3)
#define xpERROR(x) xpGPR(x,-2)
#define xpFaultStatus(x) xpERROR(x)

#define DarwinSigReturn(context)
#define SIGRETURN(context)

#include "os-linux.h"

#define PROTECT_CSTACK 1

/* Nonsense */
#define SYS_futex __NR_futex
#define PTHREAD_DESTRUCTOR_ITERATIONS 1
#define __fpurge(f)
