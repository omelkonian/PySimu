clear X data;

%% Global lambdas for all stations every 15 minutes
% i=1;
% j=1;
% 
% while (i<length(entering_global) && j<10)
%     X=entering_global(i,j);
%     current_time=timing_entering_global(i);
%     k=i+1;
%     while (timing_entering_global(k) <= current_time + minutes(15) &&...
%             k<length(entering_global))
%     
%             %append in the end of the array   
%             X=[X, entering_global(k,j)];
%             k=k+1;
%               
%     end
%       % poissfit(X) Returns the estimate of the parameter of the Poisson
%       % distribution give the data X. 
%         lambdas(i,j)=[poissfit(X)];
%         i=k;
%         
%         
%     
%     clear X;
%    %% i=i+1;
% end
% %lambdas_passengers_entering=1./mean;

%% One lambda for every station every 15 minutes
i=1;
temp=1;

timing=timing_AZU_CS_sorted;
direction=AZU_CS_entering_sorted;

for j=1:9
    time=timing(1)-minutes(10);
    while i<(length(direction) )
       X=direction(i,j);
       current_time=timing(i);
       k=i+1;
       
        
       while (timing(k) <=  time + minutes(15) ...
               && k<length(direction))
        
              X=[X;direction(k,j)];
              k=k+1;
       end
       % lambdahat = poissfit(data) returns the maximum likelihood estimate 
       % (MLE) of the parameter of the Poisson distribution, ?, given the data data.
       passengers_entering_lambdas(temp,j)=[poissfit(X)];
       temp=temp+1;
       i=k;
       clear X;
       time=time+minutes(15);
    end
    i=1;
    temp=1;
end
    
clear i temp k j;