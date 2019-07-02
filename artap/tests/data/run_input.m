% read parameters from file
x = load('input.txt');

% eval
out = x(1)^2 + x(2)^2;

% write output file
save('output.txt', 'out', '-ascii');
exit;
