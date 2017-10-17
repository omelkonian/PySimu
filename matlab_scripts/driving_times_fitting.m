% X=runtimes(:);
% X=sort(X);
% % phat(1) = a and phat(2) = b
% % The first row of pci is the lower bound of the confidence intervals
% % the last row is the upper bound
% [phat,pci]=gamfit(X);
% 
% figure;histogram(runtimes(:));xlabel('Actual runtimes');ylabel('Frequency');
% % testing
% y=gampdf(X,phat(1),phat(2));
% figure;plot(X,y);

%% For every station
alpha=0.05;

for j=1:14
   for i=1:length (runtimes)
          X(i)=runtimes(i);
   end
   [phat,pci]=gamfit(X,alpha);
   runtimes_parameters_a(j)=phat(1);
   runtimes_parameters_b(j)=phat(2);
   
end