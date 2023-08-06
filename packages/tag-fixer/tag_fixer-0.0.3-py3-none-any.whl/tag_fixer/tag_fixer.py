#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 14:41:15 2018

@author: kriskyle
"""
def tag_fixer(list1):
    
    def iterate(fixed, index, over):

        print("\n"," ".join(sent_words[:index]),fixed[index]," ".join(sent_words[index+1:]))
        response = input("Hit [return] if this tag is correct ('b' for back). Else, input corrected tag: ")
        if response == "b":
            if index == 0:
                print("First item, can't go back")
                index = 0
            else:
                index -=1
        elif response == "":
            index +=1
        else:
            fixed[index] = [sent_words[index],response.upper()]
        
        if index != over:
            iterate(fixed,index,over)
               
        return(fixed)

    sent_words = []
    to_fix = []
    
    for word,tag in list1:
        sent_words.append(word)
        to_fix.append([word,tag])
    
    
    return(iterate(to_fix,0,len(to_fix)))

def tag_fixer_sents(list_sents):
    fixed_corp = []
 
    for sent in list_sents:
        fixed_corp.append(tag_fixer(sent))
    
    return(fixed_corp)
