#!/bin/sh

set -e
digits="0 1 2 3 4 5 6 7 8 9 a b c d e f"
rm test_results.txt || true

for i0 in $digits
do
	for i1 in $digits
	do
		for i2 in $digits
		do
			for i3 in $digits
			do
				for i4 in $digits
				do
					for i5 in $digits
					do
						xxd_input="0: $i0$i1 $i2$i3 $i4$i5"
						echo $xxd_input | xxd -r >test.in
						vim -b '+set filetype=xxd | write! test.out | quit!' test.in
						if ! diff test.in test.out >/dev/null 2>/dev/null
						then
							echo $xxd_input >>test_results.txt
						fi
					done
				done
			done
		done
	done
done
