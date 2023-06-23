import numpy as np
import math

#memory size
MEMORY_SIZE =  65536

#input
address_size = 16
cache_size = 1024
cache_block_size = 64
associativity = 4
write_type_input = 0

def user_input():
	address_size = int(input("Memory Address Size\n\t(Bits):\t\t"))
	cache_size = int(input("Cache Size\n\t(Bytes):\t"))
	cache_block_size = int(input("Cache Block Size\n\t(Bytes):\t"))
	associativity = int(input("Associativity:\t\t"))
	write_type_input = int(input("Enter 0 for Write-Back;\n  1 for Write-Through:\t"))
	
#useful values?
num_cache_blocks = int(cache_size/cache_block_size)
num_cache_sets = int(num_cache_blocks/associativity)
num_index_bits = math.log(num_cache_sets,2)
num_offset_bits = math.log(cache_block_size,2)
num_tag_bits = address_size-num_index_bits-num_offset_bits 
LRU_bits = math.log(associativity,2)
bits_per_row = num_tag_bits + (cache_block_size * 8) + 1 + LRU_bits

#memory initialization
memory = np.zeros(MEMORY_SIZE)
for i in range(0, cache_size):
        if(i%4==0):
                memory[i] = int(i)
                memory[i+1] = int(int(i)/cache_block_size)

#write-allocate cache
class CacheBlock():
        bytes_ = np.zeros(cache_block_size)
        tag_ = -1
        valid_flag = -1
        dirty_flag = -1
        set_identifier = -1

class Cache():
        blocks = [CacheBlock() for i in range(num_cache_blocks)]
        tag_queue = np.zeros(associativity)

cache = Cache()

def debug():
	if (input("Manual Input (y/n):\t") =='y'):
		user_input()
	print(f"\tAddress Size:\t\t{address_size} Bits\n"+
              f"\tCache Size:\t\t{cache_size} Bytes\n"+
              f"\tCache Block Size:\t{cache_block_size} Bytes\n"+
              f"\t# of Cache Blocks:\t{int(num_cache_blocks)}\n"+
              f"\t# of Cache Sets:\t{int(num_cache_sets)}\n"+
              f"\t{associativity}-Way Associativity\n")
	if (write_type_input == 0):
		print("\tWrite-Back Cache")
	else:
		print("\tWrite-Through Cache")

	print("\nRead Test:\n")
	read_word(1152)
	read_word(2176)
	read_word(3200)
	read_word(4224)
	read_word(5248)
	read_word(7296)
	read_word(4224)
	read_word(3200)


def read_word(address):
	memory_block_index = int(address/cache_block_size)
	lower_bound = int(memory_block_index * cache_block_size)
	upper_bound = int(lower_bound + (cache_block_size-1))
	cache_slot_index = memory_block_index % associativity
	tag_number = int(memory_block_index / associativity)
	word = int(address)
	h_or_m = "miss"
	
	cache.blocks[cache_slot_index].tag_ = tag_number
	if (cache.tag_queue[associativity-1] == 0):
		cache.tag_queue[0] == tag_number
	else:	
		for i in range(0, associativity-1):
			if (cache.tag_queue[i] == tag_number):
				h_or_m = "hit"
				cache.tag_queue[i], cache.tag_queue[0] = cache.tag_queue[0], cache.tag_queue[i]
				break
		if (h_or_m == "miss"):
			for i in range (associativity-1, 0, -1):
				if (i == 0):
					cache.tag_queue[i] = tag_number             
			for i in range(associativity-2, 0, -1):
				if (cache.tag_queue[i] == 0):
					cache.tag_queue[i] = tag_number
				cache.tag_queue[associativity-1] = tag_number
			if (cache.tag_queue[associativity-1] != 0):
				cache.tag_queue[associativity-1] = tag_number
				h_or_m += " + replace"
			cache.tag_queue[associativity-1] = tag_number
		for i in range(0, cache_block_size):
			cache.blocks[cache_slot_index].bytes_[i] = memory[lower_bound+i]
	print(f"[addr={address} index={cache_slot_index} tag={tag_number}: " +
		f"read {h_or_m}; word={word} "+
		f"({lower_bound} - "
		f"{upper_bound})]")
	print(f"{cache.tag_queue}")
	return memory[cache_slot_index]

def update_cache(replacer):
	pass		
	
def write_word(address, word):
	print(f"\tAttempting Write ({word}) at [{address}]:")
	if (memory[address] != 0):
		print(f"\t\tValue already at {address}:\t{memory[address]}")
		if(input("\t\t\tOverwrite? y/n:\t") == 'y'):
			print("\t\tOverwriting")
			overwritten_value = memory[address]
			memory[address] = word
		else:
			print("\t\tOverwrite Cancelled")
		print(f"\t\tValue at {address}:\t{memory[address]}")

debug()
