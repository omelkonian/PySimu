%% leaving passengers data fitting
clear X;
%% One lambda for every station every 15 minutes

%% **** Beta can't fit the data if all values are the same. 
%% ****problem with last column where everything is 1

%transfom of leaving_global_percen to have values between [0 1]
leaving_global_percen2=leaving_global_percen./100;

i=1;
temp=1;
alpha=0.05;
for j=1:9
    while i<(length(leaving_global) )
       X=leaving_global_percen2(i,j);
       current_time=timing_leaving_global(i);
       k=i+1;
       while (timing_leaving_global(k) <= current_time + minutes(15) ...
               && k<length(leaving_global))
        
              X=[X;leaving_global_percen2(k,j)];
              k=k+1;
       end
       %beta can not be fitted if all data values are the same
       if sum(X(:))==0
           %beta can not be fitted if all data values are the same
           passengers_leaving_parameters_a(temp,j)=0;
           passengers_leaving_parameters_b(temp,j)=0;
      % elseif (X)
       else
           [phat,pci] = betafit(X,alpha);
           passengers_leaving_parameter_a(temp,j)=[phat(1)];
           passengers_leaving_parameter_b(temp,j)=[phat(2)];
       end
       
       
       temp=temp+1;
       i=k;
       clear X;
    end
    i=1;
    temp=1;
end
