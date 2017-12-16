#!/usr/bin/env python
# -*- coding: utf-8 -*-


# SOMADOR com bit carry.
def adder(bit1, bit2, cIn):
	if(bit1 == '0' and bit2 == '0' and cIn == '0'):
		return {'sum': '0', 'carry': '0'}
	if(bit1 == '0' and bit2 == '0' and cIn == '1'):
		return {'sum': '1', 'carry': '0'}
	if(bit1 == '0' and bit2 == '1' and cIn == '0'):
		return {'sum': '1', 'carry': '0'}
	if(bit1 == '0' and bit2 == '1' and cIn == '1'):
		return {'sum': '0', 'carry': '1'}
	if(bit1 == '1' and bit2 == '0' and cIn == '0'):
		return {'sum': '1', 'carry': '0'}
	if(bit1 == '1' and bit2 == '0' and cIn == '1'):
		return {'sum': '0', 'carry': '1'}
	if(bit1 == '1' and bit2 == '1' and cIn == '0'):
		return {'sum': '0', 'carry': '1'}
	if(bit1 == '1' and bit2 == '1' and cIn == '1'):
		return {'sum': '1', 'carry': '1'}

# SOMADOR COMPLETO de n bits.
def full_adder(num1, num2, n_bits):
	num3 = ''
	carry = '0'
	x = {'sum': '0', 'carry': '0'}
	
	for i in range(n_bits-1, -1, -1):
		x = adder(num1[i], num2[i], x['carry']) 
		num3 = x['sum'] + num3
	
	return num3

# Converte decimal para binário de n bits.
def dec_to_binary(decimal, n_bits):
	decimal = abs(decimal)

	binary = str(decimal%2)

	if(decimal > 1):
		binary = str(dec_to_binary(decimal/2, n_bits)) + binary
		if(len(binary) > n_bits):
			return "ERRO"
	
	return binary

# Completa os bits mais significativos para armazenar o número na memória.
def fit_in_memory(binary, n_bits):
	while n_bits > len(binary):
		binary = '0' + binary

	return binary

# Transforma um número positivo em complemento de dois em um número negativo.
def inversor(num):
	inv = ''

	for i in range(0, len(num)):
		if(num[i] == '0'):
			inv += '1'
		if(num[i] == '1'):
			inv += '0'

	one = '0'*(len(num)-1) + '1'

	inv = full_adder(inv, one, len(num))
	return inv

# Converte um decimal para complemento de dois.
def two_complement(decimal, n_bits):
	if(decimal >= 0):
		num = dec_to_binary(decimal, n_bits)
		num = fit_in_memory(num, n_bits)
	else:
		num = dec_to_binary(decimal, n_bits)
		num = fit_in_memory(num, n_bits)
		num = inversor(num)


	return num

# Inicia a memória do CPU para a multiplicação.
def init_memory(multiplier, n_bits):
	memory = '0'*n_bits +  multiplier + '0'
	return memory

# Move todos bits para a "casa" da direita.
def shit_right(memory):
	memory = memory[:-1]
	memory = memory[0] + memory
	return memory

# Deterrmina o próximo passo do algoritmo.
def next_step(memory):
	last = memory[-1]
	extra = memory[-2]

	if(last == '0' and extra == '0'):
		return 'nop'
	if(last == '0' and extra == '1'):
		return 'sub'
	if(last == '1' and extra == '0'):
		return 'sum'
	if(last == '1' and extra == '1'):
		return 'nop'

# Realiza soma do multiplicando na memória.
# O resultado é somente mostrado no domínio da ALU.
def do_sum(memory, multiplicand, n_bits):
	alu_domain = memory[:n_bits]
	alu_domain = full_adder(alu_domain, multiplicand, n_bits)

	memory = memory[n_bits:]
	memory = alu_domain + memory

	return memory

# Realiza subtração do multiplicando na memória.
# O resultado é somente mostrado no domínio da ALU.
def do_sub(memory, multiplicand, n_bits):
	multiplicand = inversor(multiplicand)

	alu_domain = memory[:n_bits]
	alu_domain = full_adder(alu_domain, multiplicand, n_bits)

	memory = memory[n_bits:]
	memory = alu_domain + memory
	return memory

# Algoritmo de multiplocação de Booth.
def booth_algorithm(multiplicand, multiplier, n_bits):

	# Coloca a memória no estado inicial da multiplicação.
	memory = init_memory(multiplier, n_bits)
	print("--- | {}".format(memory))

	# Contador de etapas (quantos bits ainda restam).
	n = n_bits

	while n > 0:

		# Decide o próximo passo.
		move = next_step(memory)

		if(move == 'nop'):
			# Não altera a memória.
			print("NOP | {}".format(memory))

		if(move == 'sum'):
			# Soma o multiplicando no domínio da ALU.
			memory = do_sum(memory, multiplicand, n_bits)
			print("SUM | {}".format(memory))

		if(move == 'sub'):
			# Subtrai o multiplicando do domínio da ALU.
			memory = do_sub(memory, multiplicand, n_bits)
			print("SUB | {}".format(memory))

		# Realiza um deslocamento da memória para a direita.
		memory = shit_right(memory)
		print(">>> | {}".format(memory))
		n -= 1
	
	# Remove o bit extra da memória.
	memory = memory[:-1]

	return memory		

# --- MAIN ----------------------------------------------------------------------------------------
def main():

	# Número de bits.
	n_bits = 4

	# Multiplicando.
	multiplicand = 3

	# Multiplicador.
	multiplier = 5

	# Converte decimal para complemento de dois.
	multiplicand = two_complement(multiplicand, n_bits)
	multiplier = two_complement(multiplier, n_bits)

	print("Multiplicand: {}".format(multiplicand))
	print("Multiplier: {}".format(multiplier))

	# Executa o algoritmo de multiplicação.
	result = booth_algorithm(multiplicand, multiplier, n_bits)
	
	# Imprime o resultado.
	print("END |  " + result)

#-------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    main()