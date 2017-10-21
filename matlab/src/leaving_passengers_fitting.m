%% Leaving passengers data fitting
%% One lambda for every station every 15 minutes
%% **** Beta can't fit the data if all values are the same. 
%% **** problem with last column where everything is 1
% i=1;
% temp=1;
% alpha=0.05;
% 
% timing=timing_AZU_CS_sorted;
% direction=AZU_CS_leaving_percen_sorted;
% 
% %transform the direction to have values between [0 1]
% direction=direction./100;
% 
% for j=1:9
%     time=timing(1)-minutes(10);
%     while i<(length(direction) )
%        X=direction(i,j);
%        current_time=timing(i);
%        k=i+1;
%        while (timing(k) <=  time + minutes(15) ...
%                && k<length(direction))
%         
%               X=[X;direction(k,j)];
%               k=k+1;
%        end
%        %beta can not be fitted if all data values are the same
%        if sum(X(:))==0
%            %beta can not be fitted if all data values are the same
%            passengers_leaving_parameter_a(temp,j)=0;
%            passengers_leaving_parameter_b(temp,j)=0;
%       
%        else
%            [phat,pci] = betafit(X,alpha);
%            passengers_leaving_parameter_a(temp,j)=[phat(1)];
%            passengers_leaving_parameter_b(temp,j)=[phat(2)];
%        end
%        
%        time=time+minutes(15);
%        temp=temp+1;
%        i=k;
%        clear X;
%     end
%     i=1;
%     temp=1;
% end
% 
% clear i temp time  alpha;


%% Leaving passengers fitting for every station for all hours for all days
% and 
% transformations into percentages

direction_leaving=CS_AZU_leaving;
direction_entering=CS_AZU_entering;

C=cell(9,1);
for i=1:length(direction_leaving)
    sum = 0;
    for j=1:9
        sum=sum+direction_entering(i,j);
        if ne(sum,0)
           p=(direction_leaving(i,j)/sum);
           C{j}=[C{j} p];
           sum=sum-direction_leaving(i,j);
        end
    end
end
exit_percentage=zeros(9,2);
for j=2:8
    [PHAT, PCI] = betafit(C{j}, 0.05);
    exit_percentage(j,:) = [PHAT(1), PHAT(2)]; 
end

clear i j p PHAT PCI sum;

%% code to save and concat after the above fitting
%% execute in command line
% AZU_CS_leaving_parameters=exit_percentage;
% CS_AZU_leaving_parameters=exit_percentage;
% leaving_parameters=[AZU_CS_leaving_parameters;CS_AZU_leaving_parameters];
