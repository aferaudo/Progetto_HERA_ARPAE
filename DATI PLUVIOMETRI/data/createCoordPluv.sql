USE [Hera]
GO

/****** Object:  Table [dbo].[coord_pluv]  ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[coord_pluv](
	[Nome] [nvarchar](70) NOT NULL,
	[lat] [float] NOT NULL,
	[long] [float] NOT NULL,
	[Territorio] [nvarchar](50) NOT NULL,
 CONSTRAINT [PK_coord_pluv] PRIMARY KEY CLUSTERED 
(
	[Nome] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
